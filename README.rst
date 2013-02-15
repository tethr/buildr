================================
Buildr: Packaging Tethr Software
================================

`Buildr` works by utilizing build servers that match the target platforms of
the packages being built.  The build script is run by a user on their local
machine.  The build script then uses `Fabric` to run the builds on each build
server.

Setting up a Build Server
-------------------------

The basic requirement for a build server is that it have a user, `buildr`, with
home directory `/home/buildr`.  The person running the build script must have
ssh key access to `buildr@<buildserver>`.  The `buildr` user on the build server
must have sudo access without having to enter a password.  Beyond that, a build
server must be in the list of build servers specified in `buildr/build.py` in 
this repository.

Setting up buildr
-----------------

::
    $ git clone git@github.com:tethr/buildr.git
    $ cd buildr
    $ virtualenv .
    $ bin/python setup.py develop

Build all packages for all platforms
------------------------------------

::

    $ bin/build all

Build one package for all platforms
-----------------------------------

::

    $ bin/build <package_name>
