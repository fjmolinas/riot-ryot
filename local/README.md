
### [`ci-boards.mk.pre`](ci-boards.mk.pre)

Use this makefile to allow flashing and testing over the ci.

#### Usage

- Set `RIOT_MAKEFILES_GLOBAL_PRE={PATH_TO_CI}/local/ci-boards.mk.pre`

This can be by setting `RIOT_MAKEFILES_GLOBAL_PRE` when calling make on RIOT
applications.

Alternatively this can be set in `~/bash.rc` so its always set. It can always
be overridden.

- Set `TRIBE_CI` when calling make to override `flash` and `term` recipes to test
  on ci.

  $ TRIBE_CI BOARD=nucleo-l152re make -C tests/xtimer_drift/ flash term

#### Targets

- list-ci-boards: lists boards connected to the ci

### [`makefiles.pre`](makefiles.pre)

Use this makefile to automatically set correct `PORT` and `DEBUG_ADAPTER_ID` for the
target `BOARD` if present in `LOCAL_BOARDS` (list of boards with custom udev rules).

To set custom udev rules follow [README.md](../README.md).

#### Usage

- Set `RIOT_MAKEFILES_GLOBAL_PRE={PATH_TO_CI}/local/makefiles.pre`

This can be by setting `RIOT_MAKEFILES_GLOBAL_PRE` when calling make on RIOT
applications.

Alternatively this can be set in `~/bash.rc` so its always set. It can always
be overridden.