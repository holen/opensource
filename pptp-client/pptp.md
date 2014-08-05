# use pptp vpn on ubuntu
install pptp client

    apt-get install pptp-linux

show ip 

    ifconfig
    ip route 
    route -n

create a vpn 

    pptpsetup --create myvpn --server 10.10.10.1 --username zhl --password zhl --start

vi /etc/ppp/peers/wvpn

    # written by pptpsetup
    pty "pptp 10.10.10.1 --nolaunchpppd"
    lock
    noauth
    nobsdcomp
    nodeflate
    name zhl
    remotename wvpn
    ipparam wvpn

vi /etc/ppp/chap-secrets

    # added by pptpsetup for wvpn
    zhl wvpn "zhl" *

show ip 

    ip a 
    route -n 
    ip route 

change default route 

    ip route del default 
    ip route add default dev ppp0
    ip route add 10.0.0.0/24 via 10.0.150.1
    route -n 
    ip route 

stop vpn 

    poff wvpn

start vpn
    
    pon wvpn

http://blog.fens.me/vpn-pptp-client-ubuntu/
