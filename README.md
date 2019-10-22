# RYOT (run your own tests)

    Give developers a bug report, and they will fix one bug

    Give them a way to run test, and they will fix bugs all their life

This project wants to provide a tool for RIOT developers to easily run tests
on their HW (development boards, multiple development boards).

The goal would be for all tests to be run on most boards at least every release,
ideally every week.

## How does it work?

To be able to scale we need to map multiple boards and be able to easily
`flash` and `test` the desired boards.

We will use `udev` rules to define `SYMLINKS` between the boards serial port
(dev/tty-board-name) and the actual serial port(dev/ttyACM* or other).
With this we can query the rest of the boards serial `dev` information
(DEBUG_ADAPTER_ID, PORT, etc.) to always flash and open a terminal on the
correct port.

The logic for this will be in [`makefiles.pre`](template/conf/makefiles.pre).

```
PORT = /dev/riot/tty$(BOARDDEF)
DEBUG_ADAPTER_ID = $(\
    shell udevadm info -q property $(PORT) |\
    sed -n ’/ID_SERIAL_SHORT/ {s/ID_SERIAL_SHORT=//p}’)
```

A local configuration will allow flashing and testing on boards on your remote
machine remotely [`makefiles.pre`](local/ci-boards.mk.pre).

```
  override FLASHER = ssh
  override FFLAGS = $(TRIBE_CI_SERVER) 'IMAGE_OFFSET=$(IMAGE_OFFSET) \
    $(TRIBE_CI_MAKE) flash-only FLASHFILE=$(TRIBE_CI_FLASHFILE)'
  SSH_UPLOAD = rsync --chmod=ugo=rwX

  define flash-recipe
    $(SSH_UPLOAD) $(FLASHFILE) $(TRIBE_CI_SERVER):$(TRIBE_CI_FLASHFILE)
    $(FLASHER) $(FFLAGS)
  endef

  RESET              = ssh
  RESET_FLAGS        = $(TRIBE_CI_SERVER) '$(TRIBE_CI_MAKE) reset'
  override TERMPROG  = ssh
  override TERMFLAGS = -t $(TRIBE_CI_SERVER) '$(TRIBE_CI_MAKE) term'
```

`tribe` team in Inria has 20+ boards and for a developer flashing on any 
board is as easy as:

    CI_RIOT_TRIBE=1 BOARD=<board> make -C examples/hello-world flash test

## [Setup](setup.md)

For install, setup and project details refer to [setup.md](setup.md).