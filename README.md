# QMK Userspace — crunchyflakes

Personal [QMK userspace](https://github.com/qmk/qmk_userspace) for a splitkb
Kyria rev3 keyboard and a Ploopy Classic 2 trackball, used daily on Linux.

## Keymaps

| Keyboard | Keymap | Purpose |
|----------|--------|---------|
| `splitkb/kyria/rev3` | [`first`](keyboards/splitkb/kyria/rev3/keymaps/first) | Daily driver — typing, programming, German text, gaming |
| `splitkb/kyria/rev3` | [`work`](keyboards/splitkb/kyria/rev3/keymaps/work) | Same as `first` (shared via `#include`), OLEDs disabled |
| `ploopyco/trackball/rev1_007` | [`default`](keyboards/ploopyco/trackball/keymaps/default) | Ploopy Classic 2 trackball, follows the Kyria's mode |

### Kyria (`first` / `work`)

Full layer diagrams and details: [keymap readme](keyboards/splitkb/kyria/rev3/keymaps/first/readme.md).

- **Colemak-DH** base layer, with QWERTY and Dvorak alternatives.
- **Home row mods** tuned with Chordal Hold, Permissive Hold and Speculative
  Hold (longer tapping term on pinky/ring; one-handed Ctrl+C / Ctrl+V allowed).
- **Thumb-driven layers**: Nav, Sym, Num and Umlaut on the thumbs; Sym + Nav
  together = Adjust (tri-layer). Layers held by two keys stay on until both
  are released.
- **German umlauts and €** via XKB compose sequences (Menu = Compose), so the
  host layout stays US; works with Shift and Caps Word.
- **Caps Word** on a thumb tap, with a 5 s idle timeout.
- **Shift+Backspace → Delete** on tap only (holding the key still gives Sym).
- **Select Word** on the Nav layer (`getreuer/select_word` module).
- **Gaming**: five layers without tap-hold keys (Colemak, QWERTY, StarCraft II,
  FPS overlay, nav/num), forced NKRO, and a Tab+Y → J combo active only there.
- **Extras**: encoders (volume, Page Up/Down), OLED layer display, and layer
  sync to the trackball over Raw HID.

### Ploopy trackball (`default`)

- Buttons: left click, middle click, right click, momentary (inverted) drag
  scroll, and mouse button 5.
- DPI options 400 / 600 / 1200 / 1600 (default 1600).
- **Follows the Kyria's mode**: the Kyria sends its mode (default / adjust /
  gaming / gaming-SC2) over Raw HID, and a host-side relay forwards it to the
  trackball, which switches layers:
  - Gaming: left button = Space, drag-scroll button = mouse button 4.
  - Gaming-SC2: extra mouse buttons 4 and 5.
  - Adjust: a button becomes `QK_BOOT` for flashing.

## Modules

[getreuer/qmk-modules](https://github.com/getreuer/qmk-modules) is included as
a git submodule in `modules/getreuer` (currently used: `select_word`). Clone
with:

```sh
git clone --recurse-submodules <repo-url>
# or, in an existing clone:
git submodule update --init --recursive
```

## Building

**GitHub Actions**: every push builds all targets listed in `qmk.json` and
attaches the firmware to the repository's Releases.

**Locally** (needs `qmk setup` done first):

```sh
qmk config user.overlay_dir="$(realpath .)"   # run from this repo
qmk userspace-compile                         # all targets
qmk compile -kb splitkb/kyria/rev3 -km first  # or a single one
```

## Flashing

Both boards are RP2040: double-tap reset (on the Kyria, once per half), then
copy the `.uf2` onto the mounted drive. On a running board, `QK_BOOT` (Kyria:
Function or Adjust layer; trackball: Adjust mode) enters the bootloader too.
