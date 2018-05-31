# Install CDH on Centos 7.4
Ref: https://www.cloudera.com/documentation/enterprise/latest/topics/installation_installation.html#concept_qpf_2d2_2p
     https://www.cloudera.com/documentation/enterprise/latest/topics/cm_ig_install_path_b.html#cmig_topic_6_6_3

## Before you again  
Install Python 2.6/2.7 and psycopg2 for Hue

    yum install python2-pip -y
    pip install psycopg2

Establish Your Cloudera Manager Repository Strategy

    wget https://archive.cloudera.com/cm5/redhat/7/x86_64/cm/cloudera-manager.repo -P /etc/yum.repos.d/

Setting hostname and set master can use sshkey login all hosts

    192.168.120.202 slave1
    192.168.120.201 master

sysctl.conf

    vm.swappiness = 0
    sysctl -p

关闭系统 大页面压缩

    echo never > /sys/kernel/mm/transparent_hugepage/enabled
    echo never > /sys/kernel/mm/transparent_hugepage/defrag
     
     # vi /etc/rc.local
     echo never > /sys/kernel/mm/transparent_hugepage/enabled
     echo never > /sys/kernel/mm/transparent_hugepage/defrag

## Install Cloudera Manager Server Software

Install the JDK from a repository

    yum install oracle-j2sdk1.7

Edit /etc/profile  
https://www.cloudera.com/documentation/enterprise/latest/topics/cdh_ig_jdk_installation.html#topic_29_1

    JAVA_HOME=/usr/java/default
    JRE_HOME=$JAVA_HOME/jre
    PATH=$PATH:$JAVA_HOME/bin
    CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
    export JAVA_HOME
    export JRE_HOME
    export PATH
    export CLASSPATH

    ln -s /usr/java/jdk.1.7.0_nn /usr/java/default

Install the Cloudera Manager Server Packages
Ref: Can download all rpm from http://archive.cloudera.com/cm5/redhat/7/x86_64/cm/5.14.3/RPMS/x86_64/ , then yum -y *.rpm

    yum install cloudera-manager-daemons cloudera-manager-server

Preparing a Cloudera Manager Server External Database, but if use mysql, turn GTID off

    /usr/share/cmf/schema/scm_prepare_database.sh mysql -h 192.168.120.201 cdh_db cdh 123456

create mysql db for hive, oozie, hue

    create database hive default character set utf8 default collate utf8_general_ci;
    grant all on hive.* to 'hive'@'%' identified by '123456';
    CREATE DATABASE `oozie` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci */;
    grant all privileges on oozie.* to 'oozie'@'localhost' identified by '123456';
    grant all privileges on oozie.* to 'oozie'@'%' identified by '123456';
    create database hue default character set utf8 default collate utf8_general_ci;
    grant all on hue.* to 'hue'@'%' identified by '123456';
    flush privileges;

Set JAVA_HOME to the directory where the JDK is installed. Add the following line to the specified files:

    export JAVA_HOME=/usr/java/jdk.1.8.0_nn
    Cloudera Manager Server host: /etc/default/cloudera-scm-server. This affects only the Cloudera Manager Server process, and does not affect the Cloudera Management Service roles.
    All hosts in an unmanaged deployment: /etc/default/bigtop-utils. You do not need to do this for clusters managed by Cloudera Manager.

    download mysql-connector-java-8.0.11.jar on master 
    mkdir /usr/share/java
    cp mysql-connector-java-8.0.11.jar /usr/share/java/mysql-connector-java.jar
    scp /usr/share/java/mysql-connector-java.jar slave:/usr/share/java/

Remove the embedded PostgreSQL properties file if it exists:

    rm /etc/cloudera-scm-server/db.mgmt.properties

Start the Cloudera Manager Server

    service cloudera-scm-server start

Use one of the following commands to install the Cloudera Manager Agent packages

    yum install cloudera-manager-agent cloudera-manager-daemons

On every cluster host, configure the Cloudera Manager Agent to point to the Cloudera Manager Server by setting the following properties in the /etc/cloudera-scm-agent/config.ini configuration file

    Property    Description
    server_host     Name of the host where Cloudera Manager Server is running.
    server_port     Port on the host where Cloudera Manager Server is running.

Start the Agents by running the following command on all hosts: 

    service cloudera-scm-agent start

# Configuring Sqoop 2 to Use PostgreSQL instead of Apache Derby
Ref: https://www.cloudera.com/documentation/enterprise/latest/topics/cdh_ig_sqoop2_configure.html  
     https://www.cloudera.com/documentation/enterprise/latest/topics/cm_ig_extrnl_pstgrs.html#cmig_topic_5_6

Install postgresql and initdb

    export LANGUAGE=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8

	yum install postgresql-server
	service postgresql initdb -E UTF8

Edit pg_hba.conf, which is usually found in /var/lib/pgsql/data

    host all all 10.29.26.60/22 md5
    host all all 127.0.0.1/32 md5

    sudo su postgres
    bash-4.2$ pg_ctl reload -D /var/lib/pgsql/data

update postgresql.conf

    listen_addresses = '*'
    shared_buffers 256MB
    wal_buffers 8MB
    checkpoint_segments 16
    checkpoint_completion_target 0.9

Restart postgresql

	service postgresql restart
    chkconfig postgresql on

Create sqoop role and sqoop db

    sudo -u postgres psql


    update pg_database set datistemplate=false where datname='template1';
    drop database Template1;
    create database template1 with owner=postgres encoding='UTF-8'
    lc_collate='en_US.utf8' lc_ctype='en_US.utf8' template template0;
    update pg_database set datistemplate=true where datname='template1';
    \c template1 VACUUM FREEZE;

	postgres=# CREATE ROLE sqoop LOGIN ENCRYPTED PASSWORD 'sqoop'
	 NOSUPERUSER INHERIT CREATEDB NOCREATEROLE;

	CREATE DATABASE "sqoop" WITH OWNER = sqoop
	 ENCODING = 'UTF8'
	 TABLESPACE = pg_default
	 LC_COLLATE = 'en_US.UTF8'
	 LC_CTYPE = 'en_US.UTF8'
	 CONNECTION LIMIT = -1;

Edit the sqoop.properties file (normally /etc/sqoop2/conf) as follows

    org.apache.sqoop.repository.jdbc.handler=org.apache.sqoop.repository.postgresql.PostgresqlRepositoryHandler
    org.apache.sqoop.repository.jdbc.transaction.isolation=READ_COMMITTED
    org.apache.sqoop.repository.jdbc.maximum.connections=50
    org.apache.sqoop.repository.jdbc.url=jdbc:postgresql://10.29.20.70:5432/sqoop
    org.apache.sqoop.repository.jdbc.driver=org.postgresql.Driver
    org.apache.sqoop.repository.jdbc.user=sqoop
    org.apache.sqoop.repository.jdbc.password=123456
    org.apache.sqoop.repository.jdbc.properties.property=value

Start the Sqoop 2 Server

	/sbin/service sqoop2-server start

Ensuring that the expected software releases are installed on hosts.        

    启动 Cloudera Management Service, ZooKeeper     
    启动 HDFS
    启动 HBase
    启动 YARN (MR2 Included)
    启动 Hive, Sqoop 2
    启动 Oozie
    启动 Hue


