# mount nfs use specific ip 

use

    ip route

so presume

    server A
    eth0 192.168.11.10/24 normal traffic
    eth1 192.168.11.11/24 nfs traffic

nfs

    eth0 192.168.11.14/24

so on server a you could have something like

    192.168.11.0 dev eth0 src 192.168.11.10
    192.168.11.0 dev eth1 src 192.168.11.11
    default via eth0 src 192.168.11.10

you could add

    ip route add 192.168.11.14/32 dev eth1 src 192.168.11.11

which says for all access to 192.168.11.14 use dev eth1 with src 192.168.11.11

so that will help with outbound traffic - inbound (from nfs to server
a) is a different matter. You will find eth0 will arp reply for
192.168.11.11 which means nfs replies will go to eth0 as well as maybe
eth1.

you could setup a permenant arp entry for 192.168.11.11 on
192.168.11.14 but .....

The other option is put the nfs server in a different subnet (not a
different ethernet broadcast segment) - so same switch different ip
network, this would stop eth0 being used over eth1
