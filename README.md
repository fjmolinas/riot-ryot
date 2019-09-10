# riot-ci-server

## install

1. Install requirements

    $ pip install requirements.txt

1. Change `SERVER` in `fabfile.py`

1. Add Authorized keys to [`authorized_keys`](template/authorized_keys)

1. Setup machine

    $ fab setup

1. Add boards to ci, follow [README.md](template/README.md)

1. Loop over 4 & 5 as needed

## template

- [boards](template/boards): fake target to call make.

- [conf](template/conf): configurations files to load pre and post RIOT makefiles.

- [`authorized_keys`]: list of public authorized ssh keys

- [`known_hosts`]: list of known host, avoid accepting ssh key first time `fab setup`
  is called.

- [`70-riotbooards.rules`]: custom udev rules for boards connected to ci. Follow
  [boards-udev] to add new ones.

## local

- [ci-boards.mk.pre](local/ci-boards.mk.pre): configuration to override `flash`
  and `term` so its done over ci.

- [makefiles.pre](local/makefiles.pre): configuration to use `LOCAL_BOARDS`
   custom udev rules to dry `PORT` and `DEBUG_ADAPTER_ID`

## scripts

- [ci_test_all.sh](scripts/ci_test_all.sh): script to lunch tests on all board
   connected to the ci or on a subset of them. It is only executed on
   applications with a test script. It can be launched on a subset of these
   applications.

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

- Notes on USB3 to USB2.

    - There are issues with usb3 and xhci as it does not allow enough devices
      I tried this manually, lets see if it survives a reboot
      `sudo setpci -H1 -d 8086:8c31 d0.l=0`
      https://www.systutorials.com/241533/how-to-force-a-usb-3-0-port-to-work-in-usb-2-0-mode-in-linux/
