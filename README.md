# RYOT (run your own tests)

    Give developers a bug report, and they will fix one bug

    Give them a way to run test, and they will fix bugs all their life

This project wants to provide a tool for RIOT developers to easily run tests
on their HW (multiple development boards).

Instead of having boards sitting on a desk or a shelf, plug in to a machine
that will allow easily running tests on all those boards. Use a different
machine than your personal machine, that way running tests doesn't mean halting
or slowing down your own work.

The goal would be for all tests to be run on most boards at least every release,
ideally every week and make this results easy to share with other RIOT developers.

## Why is it different from murdock? hil (philipp)?

Why don't I plug my boards into murdock? You could but this means relinquishing
ownership of your board to the CI. This also means setting up 1 RPI per board...
hmm maybe not what I want.

Why don't I use philipp? You can of course do this, it will enable another level
of testing, complementary. You still need to have a setup that allows running those
tests on multiple boards. How RIOT HIL handles this is with 1 RPI per board...
we don't want this.

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
  override FFLAGS = $(RYOT_CI_SERVER) 'IMAGE_OFFSET=$(IMAGE_OFFSET) \
    $(RYOT_CI_MAKE) flash-only FLASHFILE=$(RYOT_CI_FLASHFILE)'
  SSH_UPLOAD = rsync --chmod=ugo=rwX

  define flash-recipe
    $(SSH_UPLOAD) $(FLASHFILE) $(RYOT_CI_SERVER):$(RYOT_CI_FLASHFILE)
    $(FLASHER) $(FFLAGS)
  endef

  RESET              = ssh
  RESET_FLAGS        = $(RYOT_CI_SERVER) '$(RYOT_CI_MAKE) reset'
  override TERMPROG  = ssh
  override TERMFLAGS = -t $(RYOT_CI_SERVER) '$(RYOT_CI_MAKE) term'
```

### Usage Example

`tribe` team in Inria has 20+ boards and for a developer flashing on any 
board is as easy as:

    RYOT_CI=1 BOARD=<board> make -C examples/hello-world flash test

## [Setup](setup.md)

For install, setup and project details refer to [setup.md](setup.md).

## Future Work

- Find a way to share results easy
- Publish an official riot Docker flash or all-in-one image
- Always flash in docker
