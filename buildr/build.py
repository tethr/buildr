import os
import pkg_resources

from fabric import api as fab
from fabric.network import disconnect_all

USER = 'buildr'
BUILDSDIR = '/home/buildr/builds'
BUILD_SERVERS = ['localhost']


do = fab.run

class Build(object):
    commit = 'master'
    system_packages = []

    def __init__(self, name):
        self.name = name
        self.build_dir = os.path.join(BUILDSDIR, name)
        self.venv = os.path.join(self.build_dir, 'venv')
        self.src = os.path.join(self.build_dir, name)

    @fab.roles('build_servers')
    def build(self):
        do('rm -rf %s' % self.build_dir)
        do('mkdir -p %s' % self.build_dir)
        do('virtualenv %s' % self.venv)
        with fab.cd(self.venv):
            version = do('bin/python --version')
            version = version.lower().replace(' ', '')
            while version.count('.') > 1:
                version = version[:version.rindex('.')]
        site_packages = os.path.join(self.venv, 'lib', version, 'site-packages')
        with fab.cd(site_packages):
            for pkg in self.system_packages:
                # Oh what a hack!
                do('ln -s %s' % pkg)
        do('git clone %s %s' % (self.git_url, self.src))
        with fab.cd(self.src):
            do('git checkout %s' % self.commit)
        requirements = pkg_resources.resource_filename(
            self.__module__, 'requirements.txt')
        fab.put(requirements, self.build_dir)
        with fab.cd(self.build_dir):
            do('%s/bin/pip install -r requirements.txt' % self.venv)

    def __call__(self):
        fab.env.roledefs['build_servers'] = BUILD_SERVERS
        fab.env.user = USER
        fab.execute(self.build)
        disconnect_all()
