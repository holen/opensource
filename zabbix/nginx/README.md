## Monitor nginx 
Agent
    
    mkdir -p /usr/local/zabbix/bin/
    cd /usr/local/zabbix/bin
    
vim /usr/local/zabbix/bin/nginx_status.sh

    #!/bin/bash
    HOST=127.0.0.1
    PORT="801"
    
    function active {
            /usr/bin/curl "http://$HOST:$PORT/webstatus" 2>/dev/null| grep 'Active' | awk '{print $NF}'
    }
    
    function reading {
            /usr/bin/curl "http://$HOST:$PORT/webstatus" 2>/dev/null| grep 'Reading' | awk '{print $2}'
           }
    
    function writing {
            /usr/bin/curl "http://$HOST:$PORT/webstatus" 2>/dev/null| grep 'Writing' | awk '{print $4}'
           }
    
    function waiting {
            /usr/bin/curl "http://$HOST:$PORT/webstatus" 2>/dev/null| grep 'Waiting' | awk '{print $6}'
           }
    
    function accepts {
            /usr/bin/curl "http://$HOST:$PORT/webstatus" 2>/dev/null| awk NR==3 | awk '{print $1}'
           }
    
    function handled {
            /usr/bin/curl "http://$HOST:$PORT/webstatus" 2>/dev/null| awk NR==3 | awk '{print $2}'
           }
    
    function requests {
            /usr/bin/curl "http://$HOST:$PORT/webstatus" 2>/dev/null| awk NR==3 | awk '{print $3}'
           }
 
    # Run the requested function

    $1
 
chown -R zabbix.zabbix /usr/local/zabbix/bin/
    
modify /etc/zabbix/zabbix_agent.d/nginx_status.conf

    UserParameter=nginx.accepts,/usr/local/zabbix/bin/nginx_status.sh accepts
    UserParameter=nginx.handled,/usr/local/zabbix/bin/nginx_status.sh handled
    UserParameter=nginx.requests,/usr/local/zabbix/bin/nginx_status.sh requests
    UserParameter=nginx.connections.active,/usr/local/zabbix/bin/nginx_status.sh active
    UserParameter=nginx.connections.reading,/usr/local/zabbix/bin/nginx_status.sh reading
    UserParameter=nginx.connections.writing,/usr/local/zabbix/bin/nginx_status.sh writing
    UserParameter=nginx.connections.waiting,/usr/local/zabbix/bin/nginx_status.sh waiting  
    
Server 

    import nginx_status.xml
