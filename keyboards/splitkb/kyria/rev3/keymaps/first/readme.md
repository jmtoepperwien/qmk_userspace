# Kyria rev3 — `first` keymap

Personal keymap for the splitkb.com Kyria rev3 (50 keys, converted to liatris /
RP2040), used daily on Linux for typing (Colemak-DH), programming, German text,
and gaming — paired with a Ploopy trackball running the customized keymap in
[`keyboards/ploopyco/trackball/keymaps/default`](../../../../../ploopyco/trackball/keymaps/default)
from this same userspace repo (the keyboard definition itself comes from
qmk_firmware).

Design goals:

- **Colemak-DH** as the daily driver, with QWERTY and Dvorak fallbacks for
  sharing the keyboard or relearning.
- **Home row mods** on every alpha layer, tuned with the modern tap-hold stack
  (Chordal Hold, Permissive Hold, Speculative Hold).
- **Roomy thumb cluster**: all layer switches live on the thumbs; the outer
  index columns host only low-frequency keys (Adjust / F-keys). The outermost
  columns of the alpha block are intentionally left empty.
- **Gaming layers** without any tap-hold keys — pure, unmodified keys for
  games that care about timing (NKRO is forced on).
- **German umlauts** without changing the host layout, via XKB compose
  sequences, integrated with Caps Word.
- **Raw HID sync** between Kyria and Ploopy trackball: the keyboard tells the
  trackball which mode (default / adjust / gaming) is active.

The `work` keymap is a fork of this one that shares everything via
`#include` and only disables the OLEDs (office policy: no side channels on the
display).

An auto-generated drawing of the base layer with Nav/Sym/Num shown as corner
legends lives in
[`docs/keymaps/kyria/overview.svg`](../../../../../../docs/keymaps/kyria/overview.svg).

## Host setup (Linux)

Umlauts are sent as XKB compose sequences using the **Menu key as Compose**:

| Keys sent                    | Result |
|------------------------------|--------|
| `Compose` `'` `a`            | ä      |
| `Compose` `Shift+'` `a`      | Ä      |
| `Compose` `'` `o` / `u`      | ö / ü  |
| `Compose` `s` `s`            | ß      |
| `Compose` `=` `e`            | €      |

Host requirements:

- Compose must be bound to the *Menu* keysym (e.g. GNOME Tweaks → "Position of
  Compose key" → Menu, or `setxkbmap -option compose:menu`).
- The default system compose file (`/usr/share/X11/locale/*/Compose`) provides
  these sequences; nothing else to configure.
- Note: compose sequences are interpreted by the X server, so they work in
  normal applications and terminals, but not in games or apps that read raw
  keycodes.

## Base layer: Colemak-DH

```
 ,-------------------------------------------.                              ,-------------------------------------------.
 |        |   Q  |   W  |   F  |   P  |   B  |                              |   J  |   L  |   U  |   Y  | ;  : |        |
 |--------+------+------+------+------+------|                              |------+------+------+------+------+--------|
 |        |Ctrl/A| Alt/R| GUI/S| Sft/T|   G  |                              |   M  | Sft/N| GUI/E| Alt/I|Ctrl/O|        |
 |--------+------+------+------+------+------+-------------.  ,-------------+------+------+------+------+------+--------|
 |        |   Z  |   X  |   C  |   D  |   V  |Adjust|F-keys|  |F-keys|Adjust|   K  |   H  | ,  < | . >  | /  ? |        |
 `----------------------+------+------+------+------+------|  |------+------+------+------+------+----------------------'
                        | Menu | Nav/ | Sym/ | Num/ | Uml/ |  | Uml/ | Num/ | Sym/ |  Del |      |
                        |      |  Tab | Space|  Esc | CWord|  | Caps | Enter| Bksp |      |      |
                        `----------------------------------'  `----------------------------------'
```

- Home row mods: tap = letter, hold = modifier (per the keycaps' sublegends).
- **One-handed copy/paste exception**: holding `Ctrl/A` and tapping `C` or `V`
  settles as hold despite being same-hand — so `Ctrl+C` / `Ctrl+V` work with
  the left hand alone while the right hand is on the mouse.
- Thumbs, left to right: Menu (host Compose), Nav/Tab, Sym/Space, Num/Esc,
  Umlaut-hold with **tap = Caps Word toggle**; then Umlaut-hold with
  tap = Caps Lock, Num/Enter, Sym/Bksp, Delete.
- The Menu key doubles as host Compose for the umlaut sequences above.

### QWERTY and Dvorak

Same shell (thumb cluster, layer access), plain alphas with their own home row
mods. Accessed from the Adjust layer. QWERTY is also the base for the
`GAMING_QWERTY` default layer.

## Nav layer (hold either Nav/Tab thumb)

```
 ,-------------------------------------------.                              ,-------------------------------------------.
 |        |      |      |      |      |      |                              |      | PgDn | PgUp |      |      |        |
 |--------+------+------+------+------+------|                              |------+------+------+------+------+--------|
 |        |      |      |      |      |      |                              |   ←  |   ↓  |   ↑  |   →  |SelWd |        |
 |--------+------+------+------+------+------+-------------.  ,-------------+------+------+------+------+------+--------|
 |        |      |      |      |      |      |      |      |  |      | Home |  End |M Prev|M Play|M Next|VolMut| PrtSc  |
 `----------------------+------+------+------+------+------|  |------+------+------+------+------+----------------------'
                        |      |      |      |      |      |  |      |      |      |      |      |
                        `----------------------------------'  `----------------------------------'
```

**Select Word** (`SelWd`, right of the arrow cluster; from the
`getreuer/select_word` community module, wired in via `keymap.json` + the
`modules/getreuer` submodule): tap to select the word under the cursor, tap
again to extend to the next word; hold Shift while tapping to select whole
lines instead. Opposite-hand by design — left thumb holds Nav, right hand
taps. Base home-row mods stay held across the layer switch, so hold
`A` (Ctrl) + Nav + `SelWd` + `C` = copy.

## Sym layer (hold either Sym thumb)

```
 ,-------------------------------------------.                              ,-------------------------------------------.
 |        |   ~  |   <  |   >  |   '  |      |                              |   &  |   "  |   [  |   ]  |   \  |        |
 |--------+------+------+------+------+------|                              |------+------+------+------+------+--------|
 |        |   !  |   -  |   +  |   =  |   `  |                              |   $  |   _  |   (  |   )  |   %  |        |
 |--------+------+------+------+------+------+-------------.  ,-------------+------+------+------+------+------+--------|
 |        |   ^  |   #  |   *  |   @  |   0  |      |      |  |      |      |   1  |   |  |   {  |   }  |      |        |
 `----------------------+------+------+------+------+------|  |------+------+------+------+------+----------------------'
```

## Num layer (hold either Num thumb)

```
 ,-------------------------------------------.                              ,-------------------------------------------.
 |        |      |      |      |      |      |                              |      |   7  |   8  |   9  |   :  |        |
 |--------+------+------+------+------+------|                              |------+------+------+------+------+--------|
 |        | Ctrl | Alt/-| GUI/+| Sft/=|      |                              |      | Sft/4| GUI/5| Alt/6|Ctrl/0|        |
 |--------+------+------+------+------+------+-------------.  ,-------------+------+------+------+------+------+--------|
 |        |      |   /  |   *  |      |      |      |      |  |      |      |      |   1  |   2  |   3  |   -  |        |
 `----------------------+------+------+------+------+------|  |------+------+------+------+------+----------------------'
```

Digits on the right double as modifiers when held — e.g. hold `4` for Shift.

## Function layer (hold F-keys on the inner index columns, or Sym+Nav)

```
 ,-------------------------------------------.                              ,-------------------------------------------.
 |        |  F9  | F10  | F11  | F12  |      |                              |      |  F7  |  F8  |  F9  | F10  |  Boot  |
 |--------+------+------+------+------+------|                              |------+------+------+------+------+--------|
 |        |  F5  |  F6  |  F7  |  F8  |      |                              |      |  F4  |  F5  |  F6  | F11  |        |
 |--------+------+------+------+------+------+-------------.  ,-------------+------+------+------+------+------+--------|
 |        |  F1  |  F2  |  F3  |  F4  |      |      |      |  |      |      |      |  F1  |  F2  |  F3  | F12  |        |
 `----------------------+------+------+------+------+------|  |------+------+------+------+------+----------------------'
```

The right half mirrors the numpad: the digit position *is* the F-number
(`F5` sits where numpad `5` sits). Modifiers held on the base home row stay
held across the layer switch — `Alt+F4` is: hold `Alt/I`, hold F-keys, tap
`F4`.

## Adjust layer (hold Adjust on the inner index columns)

Default layer selection (left) and RGB controls (right):

- Left, top→bottom: Colemak-DH / Gaming, QWERTY / Gaming-QWERTY, Dvorak /
  Gaming-SC2, plus a `TG(_GAMING_FPS)` toggle.
- Right: RGB on/off, hue, saturation, value, effect cycling; `QK_BOOT` at the
  top-right corner (bootmate double-tap reset also works).

## Umlaut layer (hold either Umlaut thumb)

```
 ,-------------------------------------------.                              ,-------------------------------------------.
 |        |      |      |      |      |      |                              |      |      |  Ü   |      |      |        |
 |--------+------+------+------+------+------|                              |------+------+------+------+------+--------|
 |        |  Ä   |      |  ß   |      |      |                              |      |      |  €   |      |  Ö   |        |
 `-----------------------------+------+------+------+------|  |------+------+------+------+------+----------------------'
```

Umlauts sit on their Colemak-DH vowel positions — plus `€` on the `E` key
(E = Euro, no shift logic needed). Held Shift — or an active
Caps Word — capitalizes the umlauts (Caps Word stays alive through the
compose sequence and its weak Shift does the capitalization).

## Gaming layers

Five of them, all with plain (non tap-hold) keys and forced NKRO:

| Layer            | Kind            | Notes                                                            |
|------------------|-----------------|------------------------------------------------------------------|
| `GAMING`         | default layer   | Colemak-DH alphas, dedicated mods on home row / bottom left       |
| `GAMING_QWERTY`  | default layer   | plain QWERTY for games that read physical QWERTY positions        |
| `GAMING_SCII`    | default layer   | StarCraft II variant with extra Shift/Alt on the left side        |
| `GAMING_FPS`     | `TG` overlay    | near-empty; `Space` + mouse button 1 on the thumbs (aim + shoot)  |
| `GAMING_NAVNUM`  | momentary (`MO`)| numbers 1–5, arrow cluster, Esc, Pause                            |

One combo exists, **Tab+Y → J**, and it only fires on the gaming default
layers (`GAMING`, `GAMING_SCII`) via `combo_should_trigger`, so typing those
letters in prose never pays the combo buffering latency.

## Raw HID: trackball sync

On every layer change the Kyria pushes a 32-byte report
(`[report_id, mode, ...]`) where mode is `0` default, `1` adjust, `2` gaming,
`3` gaming-SCII. The Ploopy trackball keymap in this repo mirrors the same
modes and reconfigures itself accordingly (e.g. left button = Space while
gaming, extra buttons on SCII).

## Firmware details

- Tap-hold: `TAPPING_TERM 175` (+15 ms on the pinky/ring home-row mods —
  they roll slower), `QUICK_TAP_TERM 100`, `PERMISSIVE_HOLD`,
  `SPECULATIVE_HOLD`, `CHORDAL_HOLD` (+ the one-handed copy/paste exception;
  gaming layers exempt entirely).
- **Dual layer-key refcount**: QMK kills a momentary layer when *either* of
  two keys holding it is released; `post_process_record_user` counts active
  layer keys and re-asserts the layer until the last one is released (e.g.
  Sym held on both thumbs stays on until both lift).
- **Tri-layer**: holding Sym and Nav together activates Adjust — no finger
  gymnastics needed for RGB / layout switching.
- Caps Word with a 5 s idle timeout; umlaut keys and the compose keys they
  send are whitelisted so Caps Word survives umlauts.
- **Shift+Backspace → Delete** (tap of the Sym/Bksp thumb only, so
  holding it for Sym still works with Shift; real Shift only — Caps Word
  does not trigger it).
- Encoders: left = volume, right = Page Down / Page Up.
- OLEDs: master shows board, layer, and host LED locks; slave shows the Kyria
  logo. Fade out after 10 s, brightness 64. (Disabled entirely in `work`.)
- `FORCE_NKRO` for gaming.

## Building & flashing

This is a [QMK userspace](https://github.com/qmk/qmk_userspace) repo; both
keymaps are registered as build targets in `qmk.json`.

```sh
# locally (needs a qmk_firmware checkout and userspace configured)
qmk compile -kb splitkb/kyria/rev3 -km first
qmk compile -kb splitkb/kyria/rev3 -km work

# or just push: GitHub Actions builds both and attaches .uf2 files to Releases
```

Flash: double-tap the reset button, then copy the `.uf2` onto the mounted
RP2040 drive (once per half).
