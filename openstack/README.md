# Install openstack all on one single vm base on Ubuntu 14.04.2 LTS

add user

        groupadd stack
        useradd -g stack -s /bin/bash -d /home/stack -m stack
        echo "stack ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
        echo 'Defaults:stack !requiretty' >> /etc/sudoers

install git 

        apt-get install git 

vim /home/stack/start.sh

        #!/bin/sh
        DEBIAN_FRONTEND=noninteractive sudo apt-get -qqy update || sudo yum update -qy
        DEBIAN_FRONTEND=noninteractive sudo apt-get install -qqy git || sudo yum install -qy git
        sudo chown stack:stack /home/stack
        cd /home/stack
        git clone https://git.openstack.org/openstack-dev/devstack
        cd devstack
        echo '[[local|localrc]]' > local.conf
        echo ADMIN_PASSWORD=password >> local.conf
        echo MYSQL_PASSWORD=password >> local.conf
        echo RABBIT_PASSWORD=password >> local.conf
        echo SERVICE_PASSWORD=password >> local.conf
        echo SERVICE_TOKEN=tokentoken >> local.conf
        ./stack.sh

run

    su -l stack ./start.sh

# all in one machine

    [[local|localrc]]
    HOST_IP=10.0.220.1
    FLOATING_RANGE=10.0.220.192/27
    FIXED_RANGE=10.11.12.0/24
    FIXED_NETWORK_SIZE=254
    FLAT_INTERFACE=em2
    PUBLIC_INTERFACE=em1
    ADMIN_PASSWORD=stackpwd
    MYSQL_PASSWORD=stackpwd
    RABBIT_PASSWORD=stackpwd
    SERVICE_PASSWORD=stackpwd
    SERVICE_TOKEN=c2a27322b7b2fb8b9732
    
    LOGFILE=$DEST/logs/stack.sh.log
    
    LOGDAYS=2
    
    disable_service tempest
