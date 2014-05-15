# Install zabbix2.2 server

## Zabbix 2.2 for Debian 7 or see [官网][0]

Get and install deb package 

    wget http://repo.zabbix.com/zabbix/2.2/debian/pool/main/z/zabbix-release/zabbix-release_2.2-1+wheezy_all.deb
    dpkg -i zabbix-release_2.2-1+wheezy_all.deb
    apt-get update 

Instart zabbix server

    apt-get install zabbix-server-mysql zabbix-frontend-php 

Install zabbix agent 

    apt-get install zabbix-agent  

## Setting configure

Apache configuration file for Zabbix frontend is located in /etc/apache2/conf.d/zabbix   

Modify the `data.timezone`

modify the `#php_value date.timezone Europe/Riga` to `php_value date.timezone Asia/Shanghai`
    
Restart web server

    service apache2 restart 
    
## Create auto register

    configuration --> actions --> create auto registration --> add Temple link --> add host group 
    
## Monitor the web 

   create a web application
   configuration --> hosts --> create web scenario 
   create action

##  create auto register

    configure --> action --> create auto-register --> add to Linux group --> link to linux template
   
## Monitor mysql use zabbix template
Grant privileges on mysql

    GRANT PROCESS ON *.* TO 'zabbix'@'localhost' identified BY 'some_password';
    
Modify my.cnf add client user 

    [ client ]
    user = zabbix
    password = 'some_password'
    
Add zabbix mysql temple 

## Monitor mysql or see [mySQL monitoring HowTo Zabbix 2.0][1]
zabbix server
    
    import mysql.xml
    
zabbix agent 

    apt-get install php5 php5-mysql 

    mkdir /usr/local/share/zabbix/plugins/
    mv ss_get_mysql_stats.php /usr/local/share/zabbix/plugins
    mv zabbixmysql.conf /etc/zabbix/zabbix-agent.d/
        
    GRANT PROCESS ON *.* TO 'zabbix'@'localhost' identified BY 'some_password';
    
    Edit the ss_get_mysql_stats.php file, change the:
    $mysql_user = 'zabbix';
    $mysql_pass = 'some_password';
    
    Restart the agent.  
    
    To Test
    (on agent)
    zabbix_agentd -t mysql.Sort_scan
    
    (on server)
    zabbix_get -s agentip -k mysql.Sort_scan 

## Monitor mysql replication 
zabbix server 

    import zbx-mysql-replication-template.xml

zabbix agent 

    echo "UserParameter=mysql.slave_running,/usr/bin/mysql -hxx -uxx -p'xx' -e 'show slave status\G' | /usr/bin/perl -ne 'print if /Slave_\w{2,}_Running: Yes/' | /usr/bin/perl -ne 'END {print $.}'" >> /etc/zabbix/zabbix_agentd.conf
    UserParameter=mysql.check_bak,/usr/bin/tail -n 1 /var/log/bak_log/fullbak-$(date +%Y%m%d0001).log | awk -F'<|>' '{print $2}'
    
[0]:(https://www.zabbix.com/documentation/2.2/manual/installation/install_from_packages)
[1]:(https://www.zabbix.com/forum/showthread.php?t=26503)
