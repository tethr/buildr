import os
import sys

from .builds import builds


def usage():
    binname = os.path.split(os.path.abspath(sys.argv[0]))[-1]
    print >> sys.stderr, 'usage: %s [all|<pkgname>]' % binname
    sys.exit(1)


def error(msg):
    print >> sys.stderr, msg
    usage()


def main():
    if len(sys.argv) != 2:
        error("Wrong number of arguments.")

    pkgname = sys.argv[1]
    if pkgname == 'all':
        for build in builds.values():
            build()
    else:
        if pkgname not in builds:
            error("No such build: %s" % pkgname)
        builds[pkgname]()
