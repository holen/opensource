# Install pptp vpn server on centos6.5
check env

    [root@localhost ~]# cat /dev/net/tun
    cat: /dev/net/tun: File descriptor in bad state

    [root@localhost ~]# cat /dev/ppp
    cat: /dev/ppp: No such device or address

install pptpd

    rpm -Uvh http://poptop.sourceforge.net/yum/stable/rhel6/pptp-release-current.noarch.rpm
    yum install pptpd

vim /etc/ppp/options.pptpd 

    name pptpd
    refuse-pap
    refuse-chap
    refuse-mschap
    require-mschap-v2
    require-mppe-128
    ms-dns 8.8.8.8
    ms-dns 8.8.4.4
    proxyarp
    lock
    nobsdcomp 
    novj
    novjccomp
    nologfd

vim /etc/ppp/chap-secrets

    testvps pptpd "test" *

vim /etc/pptpd.conf

    option /etc/ppp/options.pptpd
    logwtmp
    localip 192.168.1.1
    remoteip 192.168.1.234-238,192.168.1.245

vim /etc/sysctl.conf

    net.ipv4.ip_forward = 1 

    $ /sbin/sysctl -p

restart pptpd

    /etc/init.d/pptpd restart

set masquerade

    /sbin/iptables -t nat -A POSTROUTING -o eth0 -s 192.168.1.0/24 -j MASQUERADE
