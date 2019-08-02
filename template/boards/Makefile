# Fake application to call make
APPLICATION = firmware
BOARD ?=  native
include RIOT/Makefile.include

ifeq (,$(filter $(BOARD),$(CI_BOARDS) native))
  $(warning Boards is not know by CI)
  $(error $(CI_BOARDS))
endif
