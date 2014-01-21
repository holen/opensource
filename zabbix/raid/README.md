# Zabbix monitor raid
Agent

    apt-get install sudo -y
    echo "zabbix ALL = (root) NOPASSWD:ALL" >> /etc/sudoers.d/zabbix
    chmod 0440 /etc/sudoers.d/zabbix 

Install raid monitor

    echo "deb http://hwraid.le-vert.net/ubuntu/ $(lsb_release -s -c) main" >>  /etc/apt/sources.list
    wget -O - http://hwraid.le-vert.net/debian/hwraid.le-vert.net.gpg.key | apt-key add -
    apt-get update 
    apt-get install megacli -y
    apt-get install hpacucli -y

zabbix-agent.conf
    
    UserParameter=raid.status,sudo /usr/sbin/megacli -LDPDInfo -aALL | grep 'Firmware state' | grep -c Online  
    UserParameter=raid.status,sudo /usr/sbin/hpacucli ctrl slot=1 pd all show status | grep -c physicaldrive
    
Import tempate xml

