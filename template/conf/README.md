
### [`makefiles.post`](makefiles.post)

Sets docker parallelism for building using `BUILD_IN_DOCKER`

### [`makefiles.pre`](makefiles.pre)

Sets correctly `PORT` and `DEBUG_ADAPTER_ID` for the target `BOARD`
(if present in `CI_BOARDS`). Also adds `makefiles.post` to `RIOT_MAKEFILES_GLOBAL_POST`.

Follow [README.md](../../README.md) to add more `BOARDS` to `CI_BOARDS`.

### [`docker.makefiles.pre`](docker.makefiles.pre)

Sets the configuration for the machine so `BUILD_IN_DOCKER` is set, the
docker image to use as well as including `docker/%` targets while this is
not in `RIOT-OS/RIOT`.

#### Targets

- `lsit-boards`: list boards connected to ci.

    $ make list-boards