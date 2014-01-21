# Zabbix monitor apache2
Enable apache status

    a2enmod status 
    /etc/init.d/apache2 reload
    
mkdir /usr/local/zabbix/bin/
    
vim /usr/local/zabbix/bin/apache-status.sh

    #!/bin/bash
    if [[ "$1" = "Workers" ]]; then
        wget --quiet -O - http://localhost/server-status?auto | grep Score | grep -o "\." | wc -l
    else
        wget --quiet -O - http://localhost/server-status?auto | head -n 9 | grep $1 | awk -F ":" '{print $2}'
    fi
 
chown -R zabbix.zabbix /usr/local/zabbix/bin/ 

chmod +x /usr/local/zabbix/bin/apache-status.sh
 
vim /etc/zabbix/zabbix-agent.d/apache-status.conf

    UserParameter=apache[*],/usr/local/zabbix/bin/apache-status.sh $1

restart zabbix-agent
