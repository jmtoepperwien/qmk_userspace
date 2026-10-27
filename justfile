kb_kyria := "splitkb/kyria/rev3"
kb_trackball := "ploopyco/trackball/rev1_007"

default: compile-all

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

format:
    fd --extension c --extension h --search-path keyboards --search-path users \
        --exec clang-format -i
