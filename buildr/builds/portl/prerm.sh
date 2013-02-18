#!/bin/sh

set -e

APP_NAME=portl

case "$1" in
    upgrade|failed-upgrade|abort-install|abort-upgrade|disappear|purge|remove)
        supervisorctl stop $APP_NAME
    ;;

    *)
        echo "prerm called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac
