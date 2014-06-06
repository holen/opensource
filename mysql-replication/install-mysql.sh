#!/bin/bash 
apt-get install mysql-server mysql-client -y 
service mysql stop

sed -i '/^#/d' /etc/mysql/my.cnf
sed -i '/^$/d' /etc/mysql/my.cnf

mkdir -p /data/mysql
mkdir -p /data/mysql-tmp
mkdir -p /data/mysql-log
chown -R mysql.root /data/mysql
chown -R mysql.root /data/mysql-tmp
chown -R mysql.root /data/mysql-log

sed -i "/device/a \ \ \/data\/mysql-log\/* rw," /etc/apparmor.d/usr.sbin.mysqld
sed -i "/device/a \ \ \/data\/mysqllog\/ r," /etc/apparmor.d/usr.sbin.mysqld
sed -i "/device/a \ \ \/data\/mysql-tmp\/* rw," /etc/apparmor.d/usr.sbin.mysqld
sed -i "/device/a \ \ \/data\/mysql-tmp\/ r," /etc/apparmor.d/usr.sbin.mysqld
sed -i "/device/a \ \ \/data\/mysql\/** rwk," /etc/apparmor.d/usr.sbin.mysqld
sed -i "/device/a \ \ \/data\/mysql\/ r," /etc/apparmor.d/usr.sbin.mysqld

sed -i 's/^datadir.*/datadir=\/data\/mysql/g' /etc/mysql/my.cnf
sed -i 's/^tmpdir.*/tmpdir=\/data\/mysql-tmp/g' /etc/mysql/my.cnf
sed -i 's/^log_error.*/log_error=\/data\/mysql-log\/error\.log/g' /etc/mysql/my.cnf
#slow_query_log  = 1
#slow_query_log_file     = /data/mysql-log/slow-query.log
