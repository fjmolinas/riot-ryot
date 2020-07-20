
### [`ci-boards.mk.pre`](ci-boards.mk.pre)

Use this makefile to allow flashing and testing over the ci.

#### Usage

- Set `RIOT_MAKEFILES_GLOBAL_PRE={CI_RIOT_TRIBE_PATH}/local/ci-boards.mk.pre`

This can be done by setting `RIOT_MAKEFILES_GLOBAL_PRE` when calling make on
RIOT applications.

Alternatively this can be set in `~/bash.rc` so its always set. It can always
be overridden.

- Set `RYOT_CI=1` when calling make to override `flash`, `term`, `reset`
recipes to test on ci.

  $ RYOT_CI=1 BOARD=nucleo-l152re make -C tests/xtimer_drift/ flash term

- Set `DISABLE_LOCAL_BOARDS=1` to disable setting `PORT` and `DEBUG_ADAPTER_ID`
for configured `BOARD`s.

#### Targets

- list-ci-boards: lists boards connected to the ci

### [`makefiles.pre`](makefiles.pre)

Use this makefile to automatically set correct `PORT` and `DEBUG_ADAPTER_ID` for the
target `BOARD` if present in `LOCAL__CONNECTED_BOARDS` (list of boards with custom udev rules).

#### Targets

- list-boards: locally connected boards

### [`local-boards.mk`](local-boards.mk)

List of configured boards. This boards should have a matching udev rule
in `template/70-riotboards.rules` respecting the common configuration of
/dev/riot/tty-$(BOARD). They must all be included into `LOCAL_BOARDS`
variable.