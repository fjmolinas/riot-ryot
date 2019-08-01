# Fake application to call make
APPLICATION = firmware
BOARD ?=  native
include RIOT/Makefile.include

ifeq (,$(filter $(BOARD) native,$(CI_BOARDS)))
  $(warning Boards is not know by CI)
  $(error $(CI_BOARDS))
endif
