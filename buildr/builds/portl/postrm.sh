#!/bin/sh

set -e

APP_NAME=portl
VAR=/var/tethr/portl

case "$1" in
    purge|remove)
        rm -rf $VAR
        supervisorctl update
    ;;

    upgrade|failed-upgrade|abort-install|abort-upgrade|disappear)
        supervisorctl update
    ;;

    *)
        echo "postrm called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac
