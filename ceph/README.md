# Ubuntu12.04 install ceph 

## Intro

Ceph的可以运行一个包含成千上万的对象存储设备（OSDS）的集群。一个最小的系统，将至少有一个ceph monitor和两个ceph osd daemons。要配置OSD集群，你必须在配置文件中的设置。 Ceph的提供了许多设置的默认值，你可以在配置文件中重写。此外，还可以在运行时使用命令行实用程序修改配置文件。  
Ceph的启动时，它会激活三个守护进程：

Ceph-OSD（强制性）:  
A Ceph OSD Daemon (Ceph OSD) stores data, handles data replication, recovery, backfilling, rebalancing, and provides some monitoring information to Ceph Monitors by checking other Ceph OSD Daemons for a heartbeat. A Ceph Storage Cluster requires at least two Ceph OSD Daemons to achieve an active + clean state when the cluster makes two copies of your data (Ceph makes 2 copies by default, but you can adjust it).  

ceph-mon（强制性）:   
A Ceph Monitor maintains maps of the cluster state, including the monitor map, the OSD map, the Placement Group (PG) map, and the CRUSH map. Ceph maintains a history (called an “epoch”) of each state change in the Ceph Monitors, Ceph OSD Daemons, and PGs.

ceph-MDS（仅强制cephfs）:  
A Ceph Metadata Server (MDS) stores metadata on behalf of the Ceph Filesystem (i.e., Ceph Block Devices and Ceph Object Storage do not use MDS). Ceph Metadata Servers make it feasible for POSIX file system users to execute basic commands like ls, find, etc. without placing an enormous burden on the Ceph Storage Cluster.   

Ceph stores a client’s data as objects within storage pools. Using the CRUSH algorithm, Ceph calculates which placement group should contain the object, and further calculates which Ceph OSD Daemon should store the placement group. The CRUSH algorithm enables the Ceph Storage Cluster to scale, rebalance, and recover dynamically.

# Preflight (a ceph-deploy admin and a 3-node ceph storage cluster)

## Ceph Deploy setup

Add the release key:

    wget -q -O- 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc' | sudo apt-key add -

Add the Ceph packages to your repository. Replace {ceph-stable-release} with a stable Ceph release (e.g., cuttlefish, dumpling, emperor, firefly, etc.). For example:

    echo deb http://ceph.com/debian-{ceph-stable-release}/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list

Update your repository and install ceph-deploy:

    sudo apt-get update && sudo apt-get install ceph-deploy
    
Generate the SSH keys 

    ssh-keygen
    ssh-copy-id {username}@node1
    ssh-copy-id {username}@node2
    ssh-copy-id {username}@node3
    
Modify the ~/.ssh/config file 

    Host node1
        Hostname node1
        User {username}
    Host node2
        Hostname node2
        User {username}
    Host node3
        Hostname node3
        User {username}
        
Modify /etc/hosts

    {ip}    node1
    {ip}    node2
    {ip}    node3

## Ceph Node setup
The admin node must be have password-less SSH access to Ceph nodes. When ceph-deploy logs in to a Ceph node as a user, that particular user must have passwordless sudo privileges.

Install NTP

    apt-get install ntp
    
Install ssh server

    apt-get install openssh-server
    
Create a ceph user on each ceph node

    useradd -d /home/{username} -m {username}
    passwd {username}
    echo "{username} ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/{username}
    chmod 0440 /etc/sudoers.d/{username}
    
# STORAGE CLUSTER (create a three ceph node cluster)

On ceph-deploy

    mkdir my-cluster
    cd my-cluster 
    
Create the cluster

    ceph-deploy new node1
    
Change the default number of replicas in the ceph 

    vim ceph.conf
    [global]
    osd pool default size=2
    
Install Ceph

    ceph-deploy install node1 node2 node3 
    
Add the initial monitor and gather the keys 

    ceph-deploy mon create-initial
    
Add two OSDs 

    ssh node1
    sudo mkdir /var/local/osd1
    
    ssh node2
    sudo mkdir /var/local/osd2
    exit
    
    ssh node3
    sudo mkdir /var/local/osd3
    exit
    
Prepare the OSDs

    #Ceph OSD Daemons write data to the disk and to journals. So you need to provide a disk for the OSD and a path to the journal partition 
    ceph-deploy osd prepare node1:/var/local/osd1:/var/local/journal1
    ceph-deploy osd prepare node2:/var/local/osd2:/var/local/journal2
    ceph-deploy osd prepare node3:/var/local/osd3:/var/local/journal3
    ceph-deploy osd activate node1:/var/local/osd1:/var/local/journal1
    ceph-deploy osd activate node2:/var/local/osd2:/var/local/journal2
    ceph-deploy osd activate node3:/var/local/osd3:/var/local/journal3
    ###
    ceph-deploy osd prepare data1:/dev/sdb
    这会缺省创建 journal分区
    /dev/sdb1 -- 存储数据
    /dev/sdb2 -- journal分区
    Journal 是底层单机存储模块用来维护事务一致性的，它是数据库领域的 redo log。
    如果你使用本地文件代替磁盘，需要后面加上就行，如下
    ceph-deploy osd prepare data1:/var/local/osd0:/var/local/journal0
 
List the disks on a node

    ceph-deploy disk list node1
    
Zap a disk in preparation 

    ceph-deploy disk zap node1:/var/local/osd1:/var/local/journal1
    #This will delete all data
    
Use ceph-deploy to copy the configuration file and admin eky to your admin node and your ceph nodes 

    ceph-deploy admin node1 node2 node3 
    sudo chmod +r /etc/ceph/ceph.client.admin.keyring

Check your cluster's health

    ceph health
    ceph osd dump
    ceph osd tree 
    ceph -w
    
## Operating my cluster

Start/Stop all daemons on a ceph node

    sudo start/stop ceph-all
    
Stop all daemons of a particular type on a ceph node 

    stop ceph-osd-all
    stop ceph-mon-all
    stop ceph-mds-all
    
start a specific daemon instance on a ceph node 

    start ceph-osd id={id}
    start ceph-mon id={hostname}
    start ceph-mds id={hostname}
    
##Monitoring a cluster 
Monitoring a cluster typically involves checking OSD status, monitor status, placement group status and metadata server status.

    ceph health
    ceph status | ceph -s 
    ceph quorum_status
    ceph mon_status
    ceph mon stat
    ceph mon dump
    ceph -w
    ceph df 
    ceph osd stat
    ceph osd dump
    ceph osd tree 
    ceph mds stat
    ceph mds dump
    ceph pg dump
    ceph pg map {pg-num}
    
##Pool
When you first deploy a cluster without creating a pool, Ceph uses the default pools for storing data. 

List pool

    ceph osd lspools
    
Override the defaults pool's replica size and number of pg

    osd pool default pg_num = 100
    osd pool default pgp_num = 100
    
    or
    
    vim /etc/ceph/ceph.conf
    [global]
    osd pool default pg_num = 250
    osd pool default pgp_num = 250
    
Set pool quotas 

    ceph osd pool set-quota {pool-name} [max_objects {obj-count}] [max_bytets {bytes}]
    Example:
        ceph osd pool set-quota data max_objects 10000
        
Delete a pool

    ceph osd pool delete {pool-name} [{pool-name} --yes-i-really-mean-it]
    
Show pool statistics

    rados df 
    
Make a snapshot of a pool

    ceph osd pool mksnap {pool-name} {snap-name}
    
Set pool values 

    ceph osd pool set {pool-name} {key} {value}
    
Get pool values

    ceph osd pool get {pool-name} {key}
    
Set the number of object replicas on a replicated pool

    ceph osd pool set {pool-name} size {num-replicas}
    Example:
        ceph osd pool set data size 3
    #The {num-replicas} includes the object itself. If you want the object and two copies of the object for a total of three instances of the object, specify 3.

Get the number of object replicas 

    ceph osd dump | grep 'replicated size'
    
How are pg use 


        obj    obj     obj     obj     obj     obj
        |       |       |       |       |       |
        _________________       _________________
                |                       |
                PG                      PG
                ________________________
                            |
                           Pool
 

        Placement Gruop1   Placement Group2
         ____________       _________
        |           |       |        |
        OSD1        OSD2    OSD2    OSD3
        
    Each Ceph OSD Daemon checks the heartbeat of other Ceph OSD Daemons every 6 seconds.jj
    
Set the number of pg

    ceph osd pool set {pool-name} pg_num {pg_num}
    ceph osd pool set {pool-name} pgp_num {pgp_num}
    #Once you increase the number of placement groups, you must also increase the number of placement groups for placement (pgp_num) before your cluster will rebalance. The pgp_num should be equal to the pg_num.
    
Get the number of pg

    ceph osd pool get {pool-name} pg_num
    
Get a cluster's pg statistics

    ceph pg dump [--format {format}]
    
Get statistics for stuck pgs

    ceph pg dump_stuck inactive|unclean|stale [--format <format>] [-t|--threshold <seconds>]
    
    Inactive:
        Placement groups cannot process reads or writes because they are waiting for an OSD with the most up-to-date data to come up and in.
        
    Unclean: 
        Placement groups contain objects that are not replicated the desired number of times. They should be recovering.
        
    Stale: 
        Placement groups are in an unknown state - the OSDs that host them have not reported to the monitor cluster in a while (configured by mon_osd_report_timeout).

Get a pg map

    ceph pg map {pg-id} 
    example
        ceph pg map 2.2d
        
Get a pgs statistics

    ceph pg {pg-id} query 

Creating

    creating --> peering  --> Active 
    
Clean

When a placement group is in the clean state, the primary OSD and the replica OSDs have successfully peered and there are no stray replicas for the placement group. Ceph replicated all objects in the placement group the correct number of times.

Degraded

When a client writes an object to the primary OSD, the primary OSD is responsible for writing the replicas to the replica OSDs. After the primary OSD writes the object to storage, the placement group will remain in a degraded state until the primary OSD has received an acknowledgement from the replica OSDs that Ceph created the replica objects successfully.

    
Scrub a pg

    ceph pg scrub {pg-id}
    
Revert lost

    ceph pg {pg-id} mark_unfound_lost revert|delete
    
Stroing/Retrieving object data

    ceph osd map {poolname} {object-name}
    
    Exercise:
    $rados put {object-name} {file-path} --pool=data
    $rados put test-object-q testfile.txt --pool=data
    $rados -p data ls 
    root@node1:~/my-cluster# ceph osd map data test-object-1
    osdmap e29 pool 'data' (0) object 'test-object-1' -> pg 0.74dc35e2 (0.22) -> up ([3,2,1], p3) acting ([3,2,1], p3)
    root@node1:~/my-cluster# cat /var/local/osd1/current/0.22_head/test-object-1__head_74DC35E2__0 
    This is a test!
    $rados rm test-object-1 --pool=data
    
Add a metadata server

    ceph-deploy mds create node1 
    
Adding monitors 

    ceph-deploy mon create node2 node3 
    ceph quorum_status --format json-pretty
    
## Block device quick start
You may use a virtual machine for your ceph-client node, but do not execute the following procedures on the same physical node as your Ceph Storage Cluster nodes (unless you use a VM)

install ceph

    ceph-deploy install ceph-client
    ceph-deploy admin ceph-client
    
On ceph-client

create a block device image 

    rbd create foo --size 4096 [-m {mon-IP}] [-k /path/to/ceph.client.admin.keyring]

On the ceph-client node, map the image to a block device.

    sudo rbd map foo --pool rbd --name client.admin [-m {mon-IP}] [-k /path/to/ceph.client.admin.keyring]

Use the block device by creating a file system on the ceph-client node.

    sudo mkfs.ext4 -m0 /dev/rbd/rbd/foo
    This may take a few moments.

Mount the file system on the ceph-client node.

    sudo mkdir /mnt/ceph-block-device
    sudo mount /dev/rbd/rbd/foo /mnt/ceph-block-device
    cd /mnt/ceph-block-device

## Ceph fs quick start
install ceph

    ceph-deploy install ceph-client
    ceph-deploy admin ceph-client
    ceph -s 
    
create a filesystem

    ceph osd pool create cephfs_data 100
    ceph osd pool create cephfs_metadata 100
    $ceph osd lspools 
    0 data,1 metadata,2 rbd,3 cephfs_data,4 cephfs_metadata,
    ceph mds newfs 3 4 --yes-i-really-mean-it
    ceph mds stat
    
create a secret file 

    cat ceph.client.admin.keyring
    copy key to ceph-client 
    cat /root/admin.secret 
    AQASXFBUgEvXAhAAD6/YUP5CvlAL/XPnTrSC/Q==
    
mount ceph fs as a kernel driver

    mkdir /mnt/mycephfs
    mount.ceph {ip}:6789:/ /mnt/mycephfs/ -o name=admin,secretfile=/root/admin.secret

##参考文献  
[ceph架构剖析](https://www.ustack.com/blog/ceph_infra/)  
[ceph存储](http://www.wzxue.com/ceph-storage/)  
[ceph官网](http://ceph.com/docs/master/start/intro/)  
[ceph译](http://blog.csdn.net/dapao123456789/article/category/2197933)  
[ceph使用](http://my.oschina.net/renguijiayi/blog/293317)  
[IBM关于ceph的说明](http://www.ibm.com/developerworks/cn/linux/l-ceph/)  
[ceph性能测试](http://tech.uc.cn/?p=1223#more-1223)  
[Ceph浅析（中）：结构、工作原理及流程](http://www.csdn.net/article/2014-04-08/2819192-ceph-swift-on-openstack-m)
