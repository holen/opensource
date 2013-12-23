# Proxmox VE cluster
Make sure that each Proxmox VE node is installed with the final hostname and IP configuration. 

## create the cluster  

Create:

    hp1# pvecm create $HOSTNAME

To check the state of cluster:

    hp1# pvecm status

## Adding nodes to the Cluster 
Add a node:

    hp2# pvecm add IP-ADDRESS-CLUSTER

For IP-ADDRESS-CLUSTER use an IP from an existing cluster node(as hp1-hostname). 

To check the state of cluster:

    hp2# pvecm status
    hp2# pvecm nodes
    
## Remove a cluster node 
Move all virtual machines out of the node 
List nodes:

    hp2# pvecm status
    
must power off the node to be removed 

    hp2# pvecm delnode hp1-hostname

## Restore the removed node
* reinstall pve
* add this node as a new node
>hp1# pvecm add hp2-IP  
>hp1# pvecm status  
>hp1# pvecm nodes  

## Re-install a cluster node
Move all virtual machines off the node.

Stop the following services:

    service pvestatd stop
    service pvedaemon stop
    service cman stop
    service pve-cluster stop

Backup /var/lib/pve-cluster/

    tar -czvf /root/pve-cluster-backup.tar.gz /var/lib/pve-cluster

Backup /root/.ssh/ 

    tar -czf /root/ssh-backup.tar.gz /root/.ssh

Scp backup
    
    scp pve-cluster-backup.tar.gz root@remote-ip:/tmp/ 
    scp ssh-backup.tar.gz  root@remote-ip:/tmp/ 

Shut server down & re-install pve.   
Make sure the hostname is the same as it was before you continue.

Scp backup 

    scp root@10.0.120.20:/root/ssh-backup.tar.gz /tmp
    scp root@10.0.120.20:/tmp/pve-cluster-backup.tar.gz /tmp
 
Stop the following services:

    service pvestatd stop
    service pvedaemon stop
    service cman stop
    service pve-cluster stop

Restore the files in /root/.ssh/

    cd /tmp
    tar -xzvf /root/ssh-backup.tar.gz

Replace /var/lib/pve-cluster/ with your backup copy

    cd /tmp
    mv /var/lib/pve-cluster /tmp/pve-cluster.origin
    tar -xzvf /root/pve-cluster-backup.tar.gz
    mv /tmp/var/lib/pve-cluster /var/lib/

Start pve-cluster & cman:

    service pve-cluster start
    service cman start

Restore the two ssh symlinks:

    ln -sf /etc/pve/priv/authorized_keys /root/.ssh/authorized_keys
    ln -sf /etc/pve/priv/authorized_keys /root/.ssh/authorized_keys.orig

Start the rest of the services:

    service pvestatd start
    service pvedaemon start
 
