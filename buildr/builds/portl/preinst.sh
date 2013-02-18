#!/bin/sh

set -e

APP_NAME=portl
LOGS=/var/log/tethr

case "$1" in
    install)
        if [ ! -d $LOGS ]; then
            mkdir -p $LOGS
        fi
    ;;

    upgrade|abort-upgrade)
    ;;

    *)
        echo "preinst called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac    
