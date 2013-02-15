from ...build import Build


class PortlBuild(Build):
    git_url = 'git://github.com/tethr/portl.git'
    build_packages = [
        'libevent-dev',
        'python-dev']
    system_packages = [
        '/usr/lib/python2.7/dist-packages/dbus/',
        '/usr/lib/python2.7/dist-packages/_dbus_bindings.so',
        '/usr/lib/python2.7/dist-packages/_dbus_glib_bindings.so',
        '/usr/lib/python2.7/dist-packages/glib/',
        '/usr/lib/python2.7/dist-packages/gobject/']
