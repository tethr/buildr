#!/bin/sh

set -e

APP_NAME=portl

case "$1" in
    configure)
        virtualenv /opt/tethr/$APP_NAME
        supervisorctl update
        STATUS=`supervisorctl status | grep portl | awk '{print $2}'`
        if [ "${STATUS:='UNKNOWN'}" = "STOPPED" ]; then
            supervisorctl start $APP_NAME 
        fi
    ;;

    abort-upgrade|abort-remove|abort-deconfigure)
    ;;

    *)
        echo "postinst called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac    
