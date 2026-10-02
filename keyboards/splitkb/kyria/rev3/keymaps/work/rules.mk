# Fork of ../first — inherit its rules, then apply the only intended differences.
include $(dir $(lastword $(MAKEFILE_LIST)))../first/rules.mk

OLED_ENABLE = no
NKRO_ENABLE = yes
