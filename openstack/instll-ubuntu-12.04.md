# Basic environment

nova-network -- Network layout

    ![network layout](http://docs.openstack.org/kilo/install-guide/install/apt/content/figures/1/a/common/figures/installguidearch-nova-networks.png) 

Controller node

    management interface(eth0):

    IP address: 10.0.0.11
    Network mask: 255.255.255.0 (or /24)
    Default gateway: 10.0.0.1

    vim /etc/hosts
    10.0.0.11   controller
    10.0.0.31   compute1

Compute node

    management interface(eth0):

    iP address: 10.0.0.31
    Network mask: 255.255.255.0 (or /24)
    Default gateway: 10.0.0.1

    The external network interface(eth1):

    auto eth1
    iface eth1 inet manual
    up ip link set dev $IFACE up
    down ip link set dev $IFACE down
