# Zabbix monitor memcache
Agent zabbix-agent.conf

    UserParameter=memcached_stats[*],/usr/local/bin/memcached.sh "$1" "$2"

/usr/local/bin/memcached.sh

    #!/bin/bash
    PORT=$1
    COMMAND=$2
    echo -e "stats\nquit" | nc 127.0.0.1 "$PORT" | grep "STAT $COMMAND " | awk '{print $3}' 
    
Import memcache tempate xml
