## setup & install

What will you need?

- find an unused machine

- make it reachable by ssh

- proceed to install

### install

1. Install requirements

    $ pip install requirements.txt

1. Change `RYOT_CI_SERVER` in `fabfile.py` and in [ci-boards.mk.pre](local/ci-boards.mk.pre)

1. Add Authorized keys to [`authorized_keys`](template/authorized_keys),
   create the file if it doesn't exist.

1. Setup machine

    $ fab setup

1. Plug, configure and qualify as many boards as you want, follow [README.md](template/README.md)

1. Loop over 4 & 5 as needed

[**Run tests, OFTEN!**](scripts/README.md)

## Usage

- connect to the ci:

    $ ssh $(RYOT_CI_SERVER)

- run tests:

    $ /builds/scripts/ci_test_all.py /builds/tmp/RIOT

- compile locally and flash/term/test on board connected to CI:

    $ RYOT_CI=1 BOARD=<ci-connected-board> make -C examples/hello-world flash term

- flash/test in docker (_note_):

Custom targets have been added to perform everything in a docker container
[#12419](https://github.com/RIOT-OS/RIOT/pull/12419). Most targets should be
available by prefixing the desired target with `docker/`, eg:

    $ BOARD=<ci-connected-board> make -C examples/hello-world docker/flash docker/term

_note_: this is still experimental, support is not integrated into RIOT master
branch, and there is no official riot image yet.

## Project structure

### template

- [boards](template/boards): fake target to call make.

- [conf](template/conf): configurations files to load pre and post RIOT makefiles.

- [`authorized_keys`]: list of public authorized ssh keys

- [`known_hosts`]: list of known host, avoid accepting ssh key first time `fab setup`
  is called.

- [`70-riotbooards.rules`]: custom udev rules for boards connected to ci. Follow
  [boards-udev] to add new ones.

### local

- [ci-boards.mk.pre](local/ci-boards.mk.pre): configuration to override `flash`
  and `term` so its done over ci.

- [makefiles.pre](local/makefiles.pre): configuration to use `LOCAL_BOARDS`
   custom udev rules to dry `PORT` and `DEBUG_ADAPTER_ID`

### scripts

- [ci_test_all.pyt](scripts/ci_test_all.pyt): script to lunch tests on all board
   connected to the ci or on a subset of them.

## boards-udev
[boards-udev]: #boards-udev

- use `udevadm info  /dev/ttyACM0` to query the udev database for information on 
  device on port `/deb/ttyACM0`.

  can also use `udevadm info --attribute-walk --name /dev/ttyACM0` for more detailed
  output when first level o 

- create a udev rule with information of the device and one parent to create a
  matching rule in [70-riotboards.rules](template/70-riotboards.rules).

- (*) udevrules can only match attributes from the device itself and a single parent.
  If more parents info is required then 

- reload rules: `udevadm control --reload-rules`

- Boards PORT are symlinked to /dev/riot/tty-[board-name] if convention in [70-riotboards.rules](template/70-riotboards.rules) is respected.

  (*) Only one board of each type is supported for the moment

### trouble-shooting

- Notes on USB3 to USB2.

    - There are issues with usb3 and xhci as it does not allow enough devices
      I tried this manually, lets see if it survives a reboot
      `sudo setpci -H1 -d 8086:8c31 d0.l=0`
      https://www.systutorials.com/241533/how-to-force-a-usb-3-0-port-to-work-in-usb-2-0-mode-in-linux/


## self hosted github runners

You can setup your own runners to run `compile_and_test_for_board.py` in a
GitHub Actions Workflow.

#### setup

1. [add a self hosted-runner](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners)
1. optional: Repeat 1 if parallel builds are desired (e.g.: on a machine with 8 cores you
   might want to configure 8 runners)
1. optional: [Configure each individual runners as a service](https://docs.github.com/en/actions/hosting-your-own-runners/configuring-the-self-hosted-runner-application-as-a-service)
1. Adapt the following [template](template/riot_ryot.yml) to your own RIOT fork `.github/workflows`
1. Adapt [`max-parallel`](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#jobsjob_idstrategymax-parallel)
and [`on`](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#on).
