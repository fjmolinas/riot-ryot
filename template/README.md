## [conf](conf)

- [`makefiles.post`](conf/makefiles.post): makefile to loaded after all
  RIOT Makefiles.

- [`makefiles.pre`](conf/makefiles.pre): sets the configuration for the
  CI.

## [boards](boards)

- [`Makefile`](boards/Makefile): fake application to call make. Allows
  using recipes like `list-boards` and collects firmware's to flash when `TRIBE_CI`
  is set see [README.md](local/README.md)

  It can possible use a different branch for flashing if non merged flasher fixes
  are needed.