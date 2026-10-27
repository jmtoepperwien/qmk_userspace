# The Kyria keymap that holds the layers (work includes it via ../first).
km := "first"

kb_kyria := "splitkb/kyria/rev3"
kb_trackball := "ploopyco/trackball/rev1_007"

default: compile-all

all: compile-all draw-all

compile-all:
    qmk userspace-compile

# Build one keymap and write compile_commands.json for clangd.
compile keyboard:
    #!/usr/bin/env bash
    set -euo pipefail
    case "{{ keyboard }}" in
        first)     qmk compile -kb {{ kb_kyria }} -km first --compiledb ;;
        work)      qmk compile -kb {{ kb_kyria }} -km work --compiledb ;;
        trackball) qmk compile -kb {{ kb_trackball }} -km default --compiledb ;;
        *) echo "Unknown keymap: {{ keyboard }}" >&2; exit 1 ;;
    esac

# Draw the Kyria keymap to docs/generated with keymap-drawer.
# Needs a qmk_firmware checkout (user.qmk_home) for `qmk c2json`.
draw keyboard:
    #!/usr/bin/env bash
    set -euo pipefail
    case "{{ keyboard }}" in
        first) out=docs/generated/kyria/kyria ;;
        *) echo "Nothing to draw for: {{ keyboard }} (only the Kyria layers are drawn)" >&2; exit 1 ;;
    esac
    mkdir -p "$(dirname "$out")"
    # Layer names must match the enum order in first/keymap.c (c2json loses
    # the #define'd names).
    layers="Colemak Qwerty Dvorak Gaming Gaming-Qwerty Gaming-SCII Gaming-FPS Gaming-NavNum Nav Sym Num Function Adjust Umlaut"
    qmk c2json -kb {{ kb_kyria }} -km {{ km }} \
        | uv run keymap -c drawer_config.yaml parse -c 12 -q - -l $layers >"$out.yaml"
    uv run keymap -c drawer_config.yaml draw "$out.yaml" >"$out.svg"
    echo "Drew $out.svg"

draw-all: (draw "first")

format:
    fd --extension c --extension h --search-path keyboards --search-path users \
        --exec clang-format -i
