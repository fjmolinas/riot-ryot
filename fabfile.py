#! /usr/bin/env python3


from fabric.api import cd, env, execute, put, task, sudo, run, runs_once
from fabric.contrib.files import sed, append


SERVER = 'ci-riot-tribe.saclay.inria.fr'


env.host_string = 'ci@{server}'.format(server=SERVER)
env.use_ssh_config = True

@task
def hello_world():
    """Check we can run a command on the server."""
    run('echo Hello World ${HOSTNAME}')


@task
def setup_sudo_and_ssh_key():
    """Meta recipe that sets up ssh and sudo no passwd"""
    _setup_authorized_keys()
    _setup_ci_nopasswd()


def _setup_authorized_keys():
    run('mkdir -p ~/.ssh')
    put('template/authorized_keys', '~/.ssh')


def _setup_ci_nopasswd():
    sudoers_tmp = '/tmp/ci_no_passwd'
    sudoers_no_passwd = '/etc/sudoers.d/ci_no_paswd'

    command = 'chown root:root {0}; mv {0} {1}'
    command = command.format(sudoers_tmp, sudoers_no_passwd)

    put('template/ci_no_passwd', sudoers_tmp)
    # Use bash -c command for sudo
    sudo('bash -c "{}"'.format(command))


@task
def disable_ssh_password_auth():
    """Disable password authentication."""
    sed('/etc/ssh/sshd_config',
        r'^.*PasswordAuthentication yes', 'PasswordAuthentication no',
        use_sudo=True)
    run('grep PasswordAuthentication /etc/ssh/sshd_config')


@task
def create_builds_directory():
    """Create builds directory"""
    sudo('mkdir -p /builds')
    sudo('chown ci:ci /builds')


@task
def setup_ci():
    """Avoid first install fail because of host validation"""
    put('template/known_hosts', '.ssh/known_hosts')


@runs_once
@task
def update():
    """apt-get update"""
    sudo('apt-get update')


@task
def dist_upgrade():
    """Upgrade packages in non interactive mode"""
    sudo('apt-get dist-upgrade -yqq')
    sudo('apt-get autoremove -yqq')


@task
def apt_cache_clean():
    """Clean package cache and autoremove packages."""
    sudo('apt-get autoremove -yqq')
    sudo('apt-get clean')


@task
def install(packages, options=''):
    """Install packages in non-interactive mode."""
    execute(update)
    sudo('apt-get install {0} -yqq {1}'.format(options, packages))


@task
def install_all_packages():
    """Meta recipe that installs all packages."""
    install_common()
    install_riot()


@task
def install_common():
    """Install common sever dependencies."""
    packages = ['vim', 'tar', 'git', 'build-essential', 'screen',
                'aptitude', 'openjdk-8-jre-headless', 'tmux']
    packages += ['python3', 'python3-dev', 'python3-pip',
                 'python3-virtualenv']
    # For script requiring python2
    packages += ['python-pip']
    install(' '.join(packages))


@task
def install_riot():
    """Install riot specific tools."""
    packages = ['make', 'docker.io', 'socat']
    packages += ['python3-serial', 'python3-pexpect']
    packages += ['python3-cryptography', 'python3-pyasn1',
                 'python3-ecdsa', 'python3-crypto']
    packages += ['python3-cryptography', 'python3-pyasn1',
                 'python3-ecdsa', 'python3-crypto']
    packages += ['protobuf-compiler', 'python-protobuf']
    # Needed for goodfet.bsl
    packages += ['python-serial']
    install(' '.join(packages))

    disable_dns_mask_for_docker()
    run('pip3 install scapy==2.4.0 --user')


@task
def install_riot_flashers():
    """Install riot specific flashing tools."""
    _install_uniflash()
    _install_py_flashers()
    _install_mspdebug()
    _install_openocd()
    _install_edbg()
    _install_avrdude()


@task
def _install_jlink():
    """Install jlink."""
    with cd('/opt'):
        sudo('wget --quiet --post-data \'accept_license_agreement=accepted&non_emb_ctr=confirmed&submit="Download software"\' https://www.segger.com/downloads/jlink/JLink_Linux_V654a_x86_64.deb')
        sudo('dpkg --install JLink_Linux_V654c_x86_64.deb')
        sudo('rm JLink_Linux_V654c_x86_64.deb')


@task
def _install_uniflash():
    """Install uniflash."""
    packages = ['libnotify4','libcanberra0','libpython2.7',
                'libgconf2-4','libusb-dev']
    install(' '.join(packages))

    with cd('/opt'):
        sudo(' wget --quiet http://software-dl.ti.com/ccs/esd/uniflash/uniflash_sl.4.6.0.2176.run')
        sudo('chmod +x uniflash_sl.4.6.0.2176.run')
        sudo('./uniflash_sl.4.6.0.2176.run --prefix /opt/ti/uniflash --mode unattended')
        sudo('rm uniflash_sl.4.6.0.2176.run')

    append('/etc/environment',
           'UNIFLASH_PATH=/opt/ti/uniflash',
           use_sudo=True)


@task
def _install_mspdebug():
    """Install mspdebug."""
    packages = ['libreadline-dev']
    install(' '.join(packages))

    sudo('mkdir -p /opt/mspdebug')
    sudo('chown ci:ci /opt/mspdebug')
    run('git clone --depth 1 https://github.com/dlbeer/mspdebug /opt/mspdebug || true')
    with cd('/opt/mspdebug'):
        run('make -j')
        sudo('make install')

@task
def _install_edbg():
    """Install mspdebug."""
    packages = ['libudev-dev']
    install(' '.join(packages))

@task
def _install_openocd():
    """Install openocd."""
    packages = ['make','pkg-config','libtool']
    packages += ['autoconf', 'automake']
    packages += ['libhidapi-hidraw0', 'libhidapi-dev']
    install(' '.join(packages))

    sudo('mkdir -p /opt/openocd')
    sudo('chown ci:ci /opt/openocd')
    run('git clone --depth 1 git://git.code.sf.net/p/openocd/code /opt/openocd || true')
    with cd('/opt/openocd'):
        run('./bootstrap')
        run('./configure --enable-stlink --enable-jlink --enable-ftdi --enable-cmsis-dap')
        run('make -j')
        sudo('make install')


@task
def _install_avrdude():
    """Install avrdude."""
    install('avrdude')


@task
def _install_py_flashers():
    """Install pyocd and esptool."""
    run('pip3 install pyocd esptool --user')


@task
def disable_dns_mask_for_docker():
    """Disable dnsmask for NetworkManager."""
    sed('/etc/NetworkManager/NetworkManager.conf',
        r'^dns=dnsmasq', '#dns=dnsmasq', use_sudo=True)
    sudo('systemctl restart NetworkManager.service')


@task
def configure_udev():
    """Configure connected boards udev rules"""
    put('template/70-riotboards.rules', '/etc/udev/rules.d/', use_sudo=True)
    sudo('udevadm control --reload')


@task
def configure_default_python():
    """RIOT used python3 as default python"""
    sudo("update-alternatives --install /usr/bin/python python /usr/bin/python3 10")


@task
def configure_ci_groups():
    """Add ci to main groups"""
    sudo('usermod -a -G docker,plugdev,dialout ci')


@task
def configure_builds_config():
    """Copy makefiles.pre and makefiles.post"""
    run('rm -rf /builds/conf')
    put('template/conf', '/builds')
    # This set makefiles.pre to avoid sourcing every time ssh is called
    append('/etc/environment',
           'RIOT_MAKEFILES_GLOBAL_PRE="/builds/conf/makefiles.pre"',
           use_sudo=True)


@task
def configure_riot_flash_tool():
    """Use latest master to flash"""
    run('mkdir -p /builds/boards')
    run('git clone https://github.com/RIOT-OS/RIOT.git /builds/boards/RIOT || true')
    run('git -C /builds/boards/RIOT fetch origin')
    run('git -C /builds/boards/RIOT checkout origin/master')
    put('template/boards/Makefile', '/builds/boards')
    run('mkdir -p /builds/boards/bin')


@task
def setup_ci_tools():
    """Copy ci scripts"""
    run('rm -rf /builds/scripts')
    put('scripts/', '/builds', mirror_local_mode=True)
    run('git init --bare ~/.gitcache')
     # Add scripts locations to env
    SCRIPTS_BASE = '/builds/scripts'
    append(
        '/etc/environment',
        'PYTHONPATH=$PYTHONPATH:{}/'.format(SCRIPTS_BASE),
        use_sudo=True
        )
    # Add compile_and_test_for_board to path
    RIOTBASE = '/builds/boards/RIOT'
    COMPILE_AND_TEST_FOR_BOARD = 'dist/tools/compile_and_test_for_board/'
    append(
        '/etc/environment',
        'PYTHONPATH=$PYTHONPATH:{}/{}'
                .format(RIOTBASE, COMPILE_AND_TEST_FOR_BOARD),
        use_sudo=True
        )


@task
def get_dockertargets_mk():
    """Fetch dockertargets makefile to use RIOT in docker"""
    # For now since this is not in RIOT master wget dockertargets.inc.mk
    # to use as makefile pre
    with cd('/builds/conf'):
        run('rm dockertargets.inc.mk || true')
        run('wget -q https://raw.githubusercontent.com/fjmolinas/RIOT/wip_docker_targets/makefiles/docker/dockertargets.inc.mk')


@task
def setup():
    """Setup the whole server.

    This can be called multiple times without problems
    """
    execute(hello_world)
    execute(setup_sudo_and_ssh_key)
    execute(disable_ssh_password_auth)
    execute(create_builds_directory)
    execute(setup_ci)

    execute(update)
    execute(dist_upgrade)
    execute(install_all_packages)
    execute(configure_udev)
    execute(configure_builds_config)
    execute(configure_ci_groups)
    execute(configure_default_python)
    execute(configure_riot_flash_tool)
    execute(setup_ci_tools)

    execute(install_riot_flashers)
    execute(get_dockertargets_mk)
