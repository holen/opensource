#!/bin/bash
PORT=$1
COMMAND=$2

echo -e "stats\nquit" | nc 127.0.0.1 "$PORT" | grep "STAT $COMMAND " | awk '{print $3}'
