
### [`makefiles.post`](makefiles.post)

Sets docker parallelism.

### [`makefiles.pre`](makefiles.pre)

Sets the configuration for the machine so  `BUILD_IN_DOCKER` is set, and the
correct set correct `PORT` and `DEBUG_ADAPTER_ID` for the target `BOARD`
(if present in `CI_BOARDS`). Also adds `makefiles.post` to `RIOT_MAKEFILES_GLOBAL_POST`.

Follow [README.md](../../README.md) to add more `BOARDS` to `CI_BOARDS`.

#### Targets

- `lsit-boards`: list boards connected to ci.

    $ make list-boards