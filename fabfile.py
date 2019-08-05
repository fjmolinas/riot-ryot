#! /usr/bin/env python3


from fabric.api import env, execute, put, task, sudo, run, runs_once
from fabric.contrib.files import sed, append


SERVER = 'ci-riot-tribe.saclay.inria.fr'


env.host_string = 'ci@{server}'.format(server=SERVER)


@task
def hello_world():
    """Check we can run a command on the server."""
    run('echo Hello World ${HOSTNAME}')


@task
def setup_sudo_and_ssh_key():
    """ """
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
    install(' '.join(packages))


@task
def install_riot():
    """Install riot specific tools."""
    packages = ['make', 'docker.io', 'openocd']
    packages += ['python3-serial', 'python3-pexpect']
    packages += ['python3-cryptography', 'python3-pyasn1',
                 'python3-ecdsa', 'python3-crypto']
    install(' '.join(packages))

    disable_dns_mask_for_docker()
    run('pip3 install scapy==2.4.0 --user')


@task
def disable_dns_mask_for_docker():
    """Disable dnsmask for NetworkManager."""
    sed('/etc/NetworkManager/NetworkManager.conf',
        r'^dns=dnsmasq', '#dns=dnsmasq', use_sudo=True)
    sudo('systemctl restart NetworkManager.service')


@task
def configure_udev():
    put('template/70-riotboards.rules', '/etc/udev/rules.d/', use_sudo=True)
    sudo('udevadm control --reload')


@task
def configure_ci_groups():
    sudo('usermod -a -G docker,plugdev,dialout ci')


@task
def configure_builds_config():
    run('rm -rf /builds/conf')
    put('template/conf', '/builds')
    # This set makefiles.pre to avoid sourcing every time ssh is called
    append('/etc/environment',
           'RIOT_MAKEFILES_GLOBAL_PRE="/builds/conf/makefiles.pre"',
           use_sudo=True)


@task
def configure_riot_flash_tool():
    run('mkdir -p /builds/boards')
    run('git clone https://github.com/RIOT-OS/RIOT.git /builds/boards/RIOT || true')
    run('git -C /builds/boards/RIOT fetch origin')
    run('git -C /builds/boards/RIOT checkout origin/master')
    put('template/boards/Makefile', '/builds/boards')
    run('mkdir -p /builds/boards/bin')


@task
def clone_ci_tools_repo():
    run('rm -rf /builds/scripts')
    put('scripts/', '/builds', mirror_local_mode=True)
    run('git init --bare ~/.gitcache')


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
    execute(configure_riot_flash_tool)
    execute(clone_ci_tools_repo)
