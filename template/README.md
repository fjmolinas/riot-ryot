## [conf](conf)

- [`makefiles.post`](conf/makefiles.post): makefile to be loaded after all
  RIOT Makefiles.

- [`makefiles.pre`](conf/makefiles.pre): sets the configuration for the
  CI.

- [`docker.makefiles.pre`](conf/makefiles.pre): sets docker configuration

## [boards](boards)

- [`Makefile`](boards/Makefile): fake application to call make. Allows
  using recipes like `list-boards` and collects firmware's to flash when `RYOT_CI`
  is set see [README.md](local/README.md)

  It can be possible use a different branch for flashing if non merged flasher
  fixes are needed.
