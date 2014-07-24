# webbench for apache
Install

    wget http://blog.zyan.cc/soft/linux/webbench/webbench-1.5.tar.gz
    tar zxvf webbench-1.5.tar.gz
    cd webbench-1.5
    make && make install
    ln -s webbench /usr/bin/

Run

    webbench -c 200 -t 10 http://xm.e.cn/

# ab

    ab -c 200 -t 10 http://xm.e.cn
    
server-status

    cat /etc/apache2/mods-enabled/status.conf | grep -v ^# | grep -v ^$
    <IfModule mod_status.c>
    <Location /server-status>
    SetHandler server-status
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1 ::1
    Allow from 10.10.10.9 
    Allow from 10.0.80.0/24
    </Location>
    ExtendedStatus On
    <IfModule mod_proxy.c>
        # Show Proxy LoadBalancer status in mod_status
        ProxyStatus On
    </IfModule>
    </IfModule>
 
access 

    http://127.0.0.1/server-status?refresh=5
