import os
import pkg_resources

from fabric import api as fab
from fabric.network import disconnect_all

USER = 'buildr'
BUILDSDIR = '/home/buildr/builds'
BUILD_SERVERS = ['192.168.2.106']
#BUILD_SERVERS = ['10.0.1.48']

do = fab.run

def which(what):
    return do('which %s' % what, warn_only=True).succeeded


class Build(object):
    commit = 'master'
    system_packages = []
    build_packages = []
    global_build_packages = [
        'gcc',
        'git',
        'make',
        'python-virtualenv',
        'rubygems']
    run_packages = []
    global_run_packages = [
        'python-virtualenv'
    ]
    global_run_packages = [
        'python-virtualenv'
    ]

    def __init__(self, name):
        self.name = name
        self.root = os.path.join(BUILDSDIR, name)
        self.install_root = os.path.join(self.root, 'install')
        self.venv = os.path.join(self.install_root, 'opt', 'tethr', name)
        self.src = os.path.join(self.root, 'src')

    @fab.roles('build_servers')
    def build(self):
        # Make sure packages are up to date
        fab.sudo('apt-get update -qq')
        fab.sudo('apt-get upgrade -qq')

        # Install any build dependencies
        for pkg in self.global_build_packages + self.build_packages:
            fab.sudo('apt-get install -qq %s' % pkg)

        # Install fpm
        if not which('fpm'):
            fab.sudo('gem install fpm')

        # Create virtual environment for build
        do('rm -rf %s' % self.root)
        do('mkdir -p %s' % self.venv)
        do('virtualenv %s' % self.venv)

        # Terrible hack where we create symbolic links from a few system
        # packages we want to use inside of our virtualenv.  This is primarily
        # because of dbus-python, which doesn't ship an installable egg.
        if self.system_packages:
            with fab.cd(self.venv):
                version = do('bin/python --version')
                version = version.lower().replace(' ', '')
                while version.count('.') > 1:
                    version = version[:version.rindex('.')]
            site_packages = os.path.join(
                self.venv, 'lib', version, 'site-packages')
            with fab.cd(site_packages):
                for pkg in self.system_packages:
                    # Oh what a hack!
                    do('ln -s %s' % pkg)

        # Install setuptools-git, so we don't lose non-Python code package
        # resources.
        with fab.cd(self.venv):
            do('bin/pip install setuptools-git')

        # Check out Python package we're actually packaging
        do('git clone %s %s' % (self.git_url, self.src))
        with fab.cd(self.src):
            do('git checkout %s' % self.commit)

            # Build sdist
            do('%s/bin/python setup.py sdist' % self.venv)
            egg = os.path.join(self.src, 'dist', do('ls dist').strip())

        # Install it and its dependencies in the virtualenv
        requirements = pkg_resources.resource_filename(
            self.__module__, 'requirements.txt')
        fab.put(requirements, self.venv)
        with fab.cd(self.venv):
            do('bin/pip install -r requirements.txt')
            do('bin/pip install %s' % egg)

        # Copy any other files that should be included
        here = os.path.dirname(requirements)
        for fname in os.listdir(here):
            path = os.path.join(here, fname)
            if os.path.isdir(path):
                fab.put(path, self.install_root)

        # Fix shebangs
        old_shebang = '#!' + os.path.join(self.venv, 'bin')
        new_shebang = '#!/opt/tethr/' + self.name + '/bin'
        with fab.cd(os.path.join(self.venv, 'bin')):
            for script in do('ls').split():
                do("sed -i -e's|%s|%s|' %s" % (
                    old_shebang, new_shebang, script))

        # Create a .deb for the whole mess
        hooks = ''
        deps = '-d ' + ' -d '.join(self.run_packages + self.global_run_packages)
        with fab.cd(self.root):
            do('fpm -s dir -t deb -n {0.name} -v {0.version} -x "*.git" '
               '-C {0.install_root} {1} {2} .'.format(
                   self, hooks, deps))

    def __call__(self):
        fab.env.roledefs['build_servers'] = BUILD_SERVERS
        fab.env.user = USER
        fab.execute(self.build)
        disconnect_all()
