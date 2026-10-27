#!/usr/bin/env python3
"""Render keymap figures (SVG) from keymap.c with keymap-drawer.

Pipeline per keymap:
  keymap.c --cpp (own #defines + layer enum expanded)--> qmk c2json --no-cpp
           --> keymap parse --> fix-ups / overview merge --> keymap draw

Outputs (docs/keymaps/<name>/):
  overview.svg       base layer with overlay layers as colored corner legends
  <layer>.svg        one per remaining layer
  (or layers.svg     all layers in one figure, for small boards)

Needs `cpp`, `qmk` (QMK_HOME → qmk_firmware checkout) and `keymap`
(keymap-drawer) on PATH, plus PyYAML. Run from anywhere:
  python3 keymap-drawer/draw.py
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "keymap-drawer" / "config.yaml"
OUT = ROOT / "docs" / "keymaps"

MOD_SYMBOLS = {"Shift": "⇧", "Ctrl": "⌃", "Alt": "⌥", "Super": "❖"}
# Hold legends of mod-taps come out as raw mod names.
MOD_NAMES = {f"{p}{s}{m}": name for m, name in
             [("CTL", "Ctrl"), ("SFT", "Shift"), ("ALT", "Alt"), ("GUI", "Super")]
             for p in ("", "MOD_") for s in ("L", "R")}
# CSS class per layer, used to color the layer keys' outlines and legends.
LAYER_CLASS = {"Nav": "nav", "Sym": "sym", "Num": "num", "Umlaut": "uml",
               "Function": "fn", "Adjust": "adj"}

TARGETS = [
    {
        "name": "kyria",
        "title": "kyria rev3 · first",
        "keyboard": "splitkb/kyria/rev3",
        "keymap_c": "keyboards/splitkb/kyria/rev3/keymaps/first/keymap.c",
        "layout": "LAYOUT_split_3x6_5",
        "columns": 12,
        "layer_names": {
            "_COLEMAK_DH": "Colemak-DH", "_QWERTY": "QWERTY", "_DVORAK": "Dvorak",
            "_GAMING": "Gaming", "_GAMING_QWERTY": "Gaming QWERTY",
            "_GAMING_SCII": "Gaming SC2", "_GAMING_FPS": "Gaming FPS",
            "_GAMING_NAVNUM": "Gaming NavNum", "_NAV": "Nav", "_SYM": "Sym",
            "_NUM": "Num", "_FUNCTION": "Function", "_ADJUST": "Adjust",
            "_UMLAUT": "Umlaut",
        },
        # Default layers: transparent there means "nothing".
        "base_layers": ["Colemak-DH", "QWERTY", "Dvorak", "Gaming",
                        "Gaming QWERTY", "Gaming SC2"],
        # Tap actions handled in process_record_user, invisible to the parser.
        "key_overrides": {"Colemak-DH": {44: {"t": "cw", "h": "Umlaut"}}},
        "overview": {"base": "Colemak-DH",
                     "corners": {"tr": "Nav", "bl": "Sym", "br": "Num"}},
        "single_figure": False,
    },
    {
        "name": "ploopy",
        "title": "ploopy classic 2",
        "keyboard": "ploopyco/trackball/rev1_007",
        "keymap_c": "keyboards/ploopyco/trackball/keymaps/default/keymap.c",
        "layout": "LAYOUT",
        "columns": 5,
        "layer_names": {
            "_DEFAULT": "Default", "_ADJUST": "Adjust", "_GAMING": "Gaming",
            "_GAMING_SCII": "Gaming SC2",
        },
        "base_layers": ["Default"],
        "key_overrides": {},
        "overview": None,
        "single_figure": True,
    },
]


def run(cmd, **kw):
    res = subprocess.run(cmd, text=True, capture_output=True, **kw)
    if res.returncode:
        sys.exit(f"{' '.join(map(str, cmd))} failed:\n{res.stderr}")
    return res.stdout


def layer_enum(src: str) -> list[str]:
    m = re.search(r"enum\s+layers\s*\{(.*?)\}", src, re.S)
    if not m:
        sys.exit("no `enum layers` found")
    body = re.sub(r"//.*|/\*.*?\*/", "", m.group(1), flags=re.S)
    return [n.split("=")[0].strip() for n in body.split(",") if n.strip()]


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def as_dict(key) -> dict:
    k = dict(key) if isinstance(key, dict) else {"t": str(key)}
    if k.get("h") in MOD_NAMES:
        k["h"] = MOD_NAMES[k["h"]]
    return k


def tap(key) -> str:
    k = as_dict(key)
    return "" if k.get("type") == "trans" else str(k.get("t", ""))


def style_key(key, base: bool) -> dict:
    """Layer keys get their layer's color; transparent on a base layer = empty."""
    k = as_dict(key)
    if k.get("type") == "trans" and base:
        return {"t": "", "type": "trans"}
    if k.get("h") in LAYER_CLASS:
        k["type"] = LAYER_CLASS[k["h"]]
    elif k.get("t") in LAYER_CLASS and "h" not in k:
        k["type"] = LAYER_CLASS[k["t"]]
    if k.get("h") in MOD_SYMBOLS:
        k["h"] = f"{MOD_SYMBOLS[k['h']]} {k['h'].lower()}"
    return k


def overview(layers: dict, base: str, corners: dict) -> list[dict]:
    keys = []
    for i, bkey in enumerate(layers[base]):
        b = as_dict(bkey)
        legends = {c: tap(layers[l][i]) for c, l in corners.items()}
        legends = {c: v for c, v in legends.items() if v}
        if b.get("h") in LAYER_CLASS or b.get("t") in LAYER_CLASS or len(tap(b)) > 1:
            keys.append(style_key(b, True))  # thumbs / named keys: centered
            continue
        if not tap(b) and not legends:
            keys.append({"t": "", "type": "trans"})
            continue
        k = {"tl": tap(b), **legends}
        if b.get("h") in MOD_SYMBOLS:
            k["h"] = MOD_SYMBOLS[b["h"]]
        keys.append(k)
    return keys


def draw_target(t: dict, tmp: Path) -> list[Path]:
    src = (ROOT / t["keymap_c"]).read_text()
    enum = layer_enum(src)
    # Expand the keymap's own #defines (and layer enum → numbers) so c2json
    # sees plain QMK keycodes; drop #includes, cpp can't resolve them here.
    stripped = re.sub(r"^\s*#\s*include.*$", "", src, flags=re.M)
    stripped = re.sub(r"enum\s+layers\s*\{.*?\};", "", stripped, flags=re.S)
    defines = [f"-D{n}={i}" for i, n in enumerate(enum)]
    pre = tmp / f"{t['name']}.c"
    pre.write_text(run(["cpp", "-P", "-x", "c", *defines, "-"], input=stripped))

    kjson = tmp / f"{t['name']}.json"
    run(["qmk", "c2json", "--no-cpp", "-kb", t["keyboard"], "-km", "draw",
         str(pre), "-o", str(kjson)])
    info = tmp / f"{t['name']}_info.json"
    info.write_text(run(["qmk", "info", "-kb", t["keyboard"], "-f", "json"]))

    names = [t["layer_names"].get(n, n) for n in enum]
    parsed = yaml.safe_load(run(["keymap", "-c", str(CONFIG), "parse",
                                 "-c", str(t["columns"]), "-q", str(kjson),
                                 "--layer-names", *names]))
    layers = {}
    for lname, rows in parsed["layers"].items():
        flat = [k for row in rows for k in (row if isinstance(row, list) else [row])]
        for pos, override in t["key_overrides"].get(lname, {}).items():
            flat[pos] = override
        layers[lname] = flat

    figures = {}  # file stem -> {layer name: keys}
    skip = set()
    if t["overview"]:
        ov = t["overview"]
        label = f"{ov['base']} + " + " · ".join(ov["corners"].values())
        figures["overview"] = {label: overview(layers, ov["base"], ov["corners"])}
        skip = {ov["base"], *ov["corners"].values()}
    styled = {l: [style_key(k, l in t["base_layers"]) for k in keys]
              for l, keys in layers.items() if l not in skip}
    if t["single_figure"]:
        figures["layers"] = styled
    else:
        figures.update({slug(l): {l: keys} for l, keys in styled.items()})

    out_dir = OUT / t["name"]
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.svg"):
        old.unlink()
    written = []
    for stem, figure_layers in figures.items():
        doc = {
            "layout": {"qmk_info_json": str(info), "layout_name": t["layout"]},
            "draw_config": {"footer_text": t["title"],
                            "n_columns": 2 if len(figure_layers) > 1 else 1},
            "layers": figure_layers,
        }
        ymap = tmp / f"{t['name']}-{stem}.yaml"
        ymap.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False))
        svg = out_dir / f"{stem}.svg"
        svg.write_text(run(["keymap", "-c", str(CONFIG), "draw", str(ymap)]))
        written.append(svg)
    return written


def main():
    with tempfile.TemporaryDirectory() as d:
        for t in TARGETS:
            for svg in draw_target(t, Path(d)):
                print(svg.relative_to(ROOT))


if __name__ == "__main__":
    main()
