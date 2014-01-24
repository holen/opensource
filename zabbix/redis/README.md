# Zabbix monitor redis
Agent install redis

    apt-get install redis-server
    
`mkdir /etc/zabbix/scripts/`  

`cp redis-status.sh /etc/zabbix/scripts`  

`chmod +x /etc/zabbix/scripts/redis-status.sh`  

vim /etc/zabbix/zabbix_agentd.d/userparameter_redis.conf 

    #Redis
    # UserParameter=redis[*],/etc/zabbix/scripts/redis-status.sh $1 $2 $3
    UserParameter=redis[*],/etc/zabbix/scripts/redis-status.sh $1 
    
`/etc/init.d/zabbix-agent restart`    

Import zabbix-redis.xml
