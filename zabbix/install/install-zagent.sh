#!/bin/bash

set -u
set -e

Host=10.0.0.11
CONF="/etc/zabbix/zabbix_agentd.conf"

cd /usr/local/src

if [ `uname -v | grep Ubuntu | wc -l` == "1" ];
then
    # wget http://repo.zabbix.com/zabbix/2.2/ubuntu/pool/main/z/zabbix-release/zabbix-release_2.2-1+precise_all.deb
    # dpkg -i zabbix-release_2.2-1+precise_all.deb
    wget http://repo.zabbix.com/zabbix/2.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_2.0-1precise_all.deb
    dpkg -i zabbix-release_2.0-1precise_all.deb
else
    # wget http://repo.zabbix.com/zabbix/2.2/debian/pool/main/z/zabbix-release/zabbix-release_2.2-1+wheezy_all.deb
    # dpkg -i zabbix-release_2.2-1+wheezy_all.deb
    wget http://repo.zabbix.com/zabbix/2.0/debian/pool/main/z/zabbix-release/zabbix-release_2.0-1wheezy_all.deb
    dpkg -i zabbix-release_2.0-1wheezy_all.deb
fi

apt-get update
apt-get install zabbix-agent -y

sed -i '/UnsafeUserParameters=/a\  UnsafeUserParameters=1' $CONF
sed -i 's/Server=.*/Server=$Host/g' $CONF
sed -i 's/ServerActive=.*/ServerActive=$Host/g' $CONF
sed -i "s/Hostname=.*/Hostname=$HOSTNAME/g" $CONF

echo "UserParameter=raid.status,sudo /usr/sbin/megacli -LDPDInfo -aALL | grep 'Firmware state' | grep -c Online" >> $CONF

apt-get install sudo -y 
echo "zabbix ALL = (root) NOPASSWD:ALL" >> /etc/sudoers.d/zabbix
chmod 0440 /etc/sudoers.d/zabbix

/etc/init.d/zabbix-agent restart

# Instart zabbix server
# apt-get install zabbix-server-mysql zabbix-frontend-php -y
