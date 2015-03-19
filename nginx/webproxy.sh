#!/bin/bash

ROOTDIR="/data/nginx/"
MFILE="maintenance.html"
WEBSITE=$1
COMMAND=$2

help() {
    echo "wcnproxy WEBSITE COMMAND"
    echo "WEBSITE: app.e.cn e.cn"
    echo "COMMAND: status start stop"
    exit 255
}

if [[ $WEBSITE != "app.e.cn" ]] && [[ $WEBSITE != "e.cn" ]]; then
    echo "";
    help
fi

case $COMMAND in
status)
    if [[ -f "$ROOTDIR/$WEBSITE/$MFILE" ]]; then
        echo "$WEBSITE is in maintenance status"
    else
        echo "$WEBSITE is running"
    fi
    ;;
start)
    if [[ -L "$ROOTDIR/$WEBSITE/$MFILE" ]]; then
        unlink "$ROOTDIR/$WEBSITE/$MFILE"
    fi
    service nginx reload
    ;;
stop)
    ln -s "$ROOTDIR/$WEBSITE/$MFILE.disabled" "$ROOTDIR/$WEBSITE/$MFILE"
    ;;
*)
    help
esac


