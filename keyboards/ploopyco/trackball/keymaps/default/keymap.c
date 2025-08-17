/* Copyright 2020 Christopher Courtney, aka Drashna Jael're  (@drashna) <drashna@live.com>
 * Copyright 2019 Sunjun Kim
 * Copyright 2020 Ploopy Corporation
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#include QMK_KEYBOARD_H
#include "raw_hid.h"


typedef struct __attribute__((packed)) {
  uint8_t report_id;
  uint8_t layer;
  uint8_t command;
  uint8_t argument;
  uint8_t reserved[29];
} data_config_t;


enum layers {
    _DEFAULT = 0,
    _ADJUST,
    _GAMING,
    _GAMING_SCII,
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [_DEFAULT] = LAYOUT( /* Base */
        QK_MOUSE_BUTTON_1, QK_MOUSE_BUTTON_3, QK_MOUSE_BUTTON_2,
          DRAG_SCROLL, QK_MOUSE_BUTTON_5
    ),
    [_ADJUST] = LAYOUT(
        _______, _______, _______,
          _______, QK_BOOT
    ),
    [_GAMING] = LAYOUT(
        KC_SPACE, _______, _______,
          QK_MOUSE_BUTTON_4, _______
    ),
    [_GAMING_SCII] = LAYOUT(
        _______, _______, _______,
          QK_MOUSE_BUTTON_5, QK_MOUSE_BUTTON_4
    ),

};


enum common_layers {
    G_DEFAULT = 0,
    G_ADJUST = 1,
    G_GAMING = 2,
    G_GAMING_SCII = 3,
};

void set_layer_using_common(enum common_layers layer) {
    layer_move(_DEFAULT);
    switch (layer) {
        case G_ADJUST:
            layer_on(_ADJUST);
            return;
        case G_GAMING:
            layer_on(_GAMING);
            return;
        case G_GAMING_SCII:
            layer_on(_GAMING_SCII);
            return;
        default:
            return;
    }
}

void raw_hid_receive(uint8_t *data, uint8_t length) {
    data_config_t *data_config = (data_config_t*)data;
    set_layer_using_common(data_config->layer);
    raw_hid_send(data, length);
}
