Download zabbix source pkg

    cd /opt/
    wget http://repo.zabbix.com/zabbix/2.4/ubuntu/pool/main/z/zabbix/zabbix_2.4.5.orig.tar.gz
    tar zxvf zabbix_2.4.5.orig.tar.gz 
    cd zabbix-2.4.5/

add user

    groupadd zabbix
    useradd -g zabbix zabbix 

install mysql

    apt-get install mysql-server mysql-client
    vim /etc/mysql/my.cnf 
    default-storage-engine = innodb
    innodb_file_per_table
    collation-server = utf8_general_ci
    init-connect = 'SET NAMES utf8'
    character-set-server = utf8
    bind-address            = 0.0.0.0

    service mysql restart

    mysql -uroot -p
    shell> mysql -uroot -p<password>
    mysql> create database zabbix character set utf8 collate utf8_bin;
    mysql> grant all privileges on zabbix.* to zabbix@localhost identified by '<password>';
    mysql> quit;
    shell> mysql -uzabbix -p<password> zabbix < database/mysql/schema.sql
    # stop here if you are creating database for Zabbix proxy
    shell> mysql -uzabbix -p<password> zabbix < database/mysql/images.sql
    shell> mysql -uzabbix -p<password> zabbix < database/mysql/data.sql

install snmp

    apt-get install snmp snmpd libsnmp-base libsnmp-dev 
    vim /etc/snmp/snmpd.conf
    agentAddress  udp:0.0.0.0:161
    lsof -i:161
    service snmpd restart
    snmpwalk -v 2c -c public 10.10.10.108

configure && make install

    cd /opt/zabbix-2.4.5/
    apt-get install make gcc mysql-devel libghc-hsql-mysql-dev libxml2 libxml2-dev libcurl4-openssl-dev 
    ./configure --help
    ./configure --enable-server --enable-agent --with-mysql --enable-ipv6 --with-net-snmp --with-libcurl --with-libxml2
    make install 

install php web

    apt-get install apache2 php5 php5-mysql php5-gd
    mkdir /var/www/html/zabbix
    cd frontends/php/
    cp -a . /var/www/html/zabbix/
    vim /etc/apache2/sites-enabled/000-default.conf 
    <VirtualHost *:80>
      DocumentRoot /var/www/html
      <Directory />
        Options FollowSymLinks
        AllowOverride All
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
    service apache2 restart

config php5 

    vim apache2/php.ini cli/php.ini 
    
    max_execution_time = 300
    max_input_time = 300
    date.timezone = Asia/Shanghai
    post_max_size = 16M

    service apache2 restart

