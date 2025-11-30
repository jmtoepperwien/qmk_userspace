ifeq ($(strip $(OCEAN_DREAM_ENABLE)), yes)
	SRC += ocean_dream/ocean_dream.c
	WPM_ENABLE = yes
	OPT_DEFS += -DOCEAN_DREAM_ENABLE
endif
