ifneq (, $(filter openmote-b,$(BOARD)))
  PROGRAMMER ?= jlink
endif
