# elasticsearch logstash kibana redis
one machine install soft: jdk logstash kibana apache redis elasticsearch
another machine install soft: jdk logstash
## Install java

    download jdk-7u51-linux-x64.tar.gz
    mkdir -p /data/java/
    tar zxvf /data/jdk-7u51-linux-x64.tar.gz -C /data/java/
    vim /etc/profile
    export JAVA_HOME=/data/java/jdk1.7.0_51
    export JRE_HOME=/data/java/jdk1.7.0_51/jre
    export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
    export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH

    source /etc/profile
    java -version

    echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf
    #指定了内核针对内存分配的策略，其值可以是0、1、2
    sysctl -p

## Install redis
Download and install

    apt-get install make gcc
    echo never > /sys/kernel/mm/transparent_hugepage/enabled
    echo 511 > /proc/sys/net/core/somaxconn
    wget http://download.redis.io/releases/redis-2.8.13.tar.gz
    tar zxvf redis-2.8.13.tar.gz
    cd redis-2.8.13
    cd deps
    make hiredis lua jemalloc linenoise
    cd ..
    make
    make install

    mkdir -p /data/redis/db
    mkdir -p /data/redis/bin
    mkdir -p /data/redis/log
    mkdir -p /data/redis/etc

start shell

    cd /data/redis/
    wget https://github.com/ijonas/dotfiles/raw/master/etc/init.d/redis-server
    mv redis-server ./bin/

configure

    vim /data/redis/etc/redis.conf
        daemonize yes
        pidfile /var/run/redis.pid
        port 6379
        timeout 0
        loglevel verbose
        logfile /data/redis/log/redis.log
        dbfilename dump.rdb
        dir /data/redis/db/
        activerehashing yes

grant

    ln -s /data/redis/bin/redis-server /etc/init.d/redis-server
    ln -s /data/redis/etc/redis.conf /etc/redis.conf
    chmod +x /etc/init.d/redis-server
    update-rc.d redis-server defaults
    useradd -M redis -s /sbin/nologin
    chown -R redis.redis /data/redis #
    service redis-server restart

test

    /usr/local/bin/redis-server --loglevel verbose

    redis-cli set foo bar
    redis-cli get foo
    redis-cli keys '*'
    redis-cli llen logstash
    redis-cli lrange logstash 0 1
    redis-cli lpop logstash

## Install elasticsearch

    cd /data/
    wget wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.2.tar.gz
    tar zxvf elasticsearch-1.3.2.tar.gz
    mv elasticsearch-1.3.2 elasticsearch
    /data/elasticsearch/bin/elasticsearch -f &

test

    curl localhost:9200/_search?pretty=true
    curl -XDELETE localhost:9200/logstash-2014.02.17
    curl -s http://127.0.0.1:9200/_status?pretty=true | grep logstash
    curl -gs -XGET "http://localhost:9200/logstash-*/_search?pretty&q=type:example"

## Install kibana
Install apache

    apt-get install apache2 apache2-mpm-prefork php5 libapache2-mod-php5
    echo 'ServerName kibana' > /etc/apache2/httpd.conf
    mkdir -p /data/www/
    chown -R www-data.www-data /data/www

    vim /etc/apache2/sites-available/kibana

    <VirtualHost *:80>
            DocumentRoot /data/www/kibana
            ServerName kibana
            <Directory />
                    Options  Indexes  FollowSymLinks  +Includes
                    AllowOverride All
                    Order deny,allow
                    Deny from all
                    Allow from 10.0.80.0/24
                    AddType text/html .shtml
                    AddOutputFilter INCLUDES .shtml
                    DirectoryIndex index.php index.html
            </Directory>
            LogLevel warn
            ErrorLog ${APACHE_LOG_DIR}/kibana.error.log
            CustomLog ${APACHE_LOG_DIR}/kibana.access.log combined
    </VirtualHost>

    a2enmod rewrite
    a2dissite default
    a2ensite kibana

Configure kibana

    wget https://download.elasticsearch.org/kibana/kibana/kibana-3.1.0.tar.gz
    tar zxvf /data/kibana-3.0.0milestone4.tar.gz -C /data/www/
    mv kibana-3.1.0 kibana
    chown -R www-data.www-data /data/www
    service apache2 restart

## logstash
Download logstash

    cd /data/
    wget https://download.elasticsearch.org/logstash/logstash/logstash-1.4.2.tar.gz
    tar zxvf logstash-1.4.2.tar.gz
    mv logstash-1.4.2 logstash
    ./logstash/bin/plugin install contrib # https://download.elasticsearch.org/logstash/logstash/logstash-contrib-1.4.2.tar.gz
    ./logstash/bin/logstash agent -f logstash.apache.conf &

Write apache log to redis db on client

    vim logstash.apache.conf
    input {
        file {
            type => 'apache-access'
            path => '/var/log/apache2/access.log'
        }
    }
    filter {
      grok {
        type => "apache-access"
        pattern => "%{COMBINEDAPACHELOG}"
      }
    }
    output {
        redis {
            host => '10.0.140.75'
            port => '6379'
            data_type => 'list'
            key => 'apache-access'
        }
    }

start

    java -jar /data/logstash-1.3.3-flatjar.jar agent -f /data/logstash.index.conf -verbose &

Write to kibana(web) on server

    vim logstash.index.conf
    input {
            redis {
                    host => "10.0.140.75"
                    data_type => "list"
                    port => "6379"
                    key => "apache-access"
                    type => "redis-input"
            }
    }

    output {
            elasticsearch_http {
                    host => "10.0.140.75"
                    port => "9200"
            }
    }

## access

    http://yourserver:9200

## rsyslog
client

    apt-get update
    apt-get install rsyslog

    #send log to 10.0.140.75
    vim /etc/rsyslog.d/50-default.conf
    *.* @10.0.140.75
    /etc/init.d/rsyslog restart

server

    apt-get update
    apt-get install rsyslog

    #open udp514 port,allow 10.0.140.0/24 access
    vim /etc/rsyslog.conf
    $ModLoad immark
    $ModLoad imudp
    $UDPServerRun 514
    $AllowedSender UDP, 127.0.0.1, 10.0.140.0/24

    vim /etc/default/rsyslog
    RSYSLOGD_OPTIONS="-c5 -r -x"

    #定义rsyslog模板,带客户机ip
    vim /etc/rsyslog.d/50-default.conf

    $template myFormat, "%fromhost-ip% %rawmsg%\n"
    *.* /data/rsyslog.log;myFormat

    /etc/init.d/rsyslog restart

    ####日志轮转
    vim /etc/logrotate.d/rsyslog

    /data/rsyslog*.log
    {
      rotate 7
      daily
      missingok
      notifempty
      compress
      delaycompress
      sharedscripts
      postrotate
        /bin/kill -HUP `cat /var/run/syslogd.pid 2> /dev/null` 2> /dev/null || true
        /bin/kill -HUP `cat /var/run/rsyslogd.pid 2> /dev/null` 2> /dev/null || true
      endscript
    }

## 参考文献：

[grokdebug](http://grokdebug.herokuapp.com/)
[elasticsearch_download](http://www.elasticsearch.org/download)
[logstash_doc](http://logstash.net/docs/1.4.2/)
[ Kibana+Logstash+Elasticsearch 日志查询系统](http://enable.blog.51cto.com/747951/1049411)
[kibana中文指南](http://kibana.logstash.es/content/)
