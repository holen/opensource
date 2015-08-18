# Hadoop Cluster Setup
Installation

    master: NameNode (one machine)
            ResourceManager (one machine, can include web app proxy server and MapReduce)
    slave:  DataNode and node Manager (the test of the machine)

Cat /etc/hosts

    10.0.140.37     master
    10.0.140.38     resourcemanager
    10.0.140.39     slave1
    10.0.140.40     slave2

Prerequisites

    apt-get install openjdk-7-jdk
    export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
    download hadoop-2.7.1.tar.gz
    tar zxvf hadoop-2.7.1.tar.gz
    mv hadoop-2.7.1 /usr/local/hadoop
    export HADOOP_PREFIX=/usr/local/hadoop

User Account for Hadoop Daemons

    User:Group          Daemons
    hdfs:hadoop         NameNode,Secondary NameNode,JournalNode,DataNode
    yarn:hadoop         ResourceManager,nodeManager
    mapred:hadoop       MapReduce JobHistory Server

Permissions for both HDFS and local fileSystem paths

    Filesystem  Path                                        User:Group      Permissions
    local       dfs.namenode.name.dir                       hdfs:hadoop     drwx------
    local       dfs.datanode.data.dir                       hdfs:hadoop     drwx------
    local       $HADOOP_LOG_DIR                             hdfs:hadoop     drwxrwxr-x
    local       $YARN_LOG_DIR                               yarn:hadoop     drwxrwxr-x
    local       yarn.nodemanager.local-dirs                 yarn:hadoop     drwxr-xr-x
    local       yarn.nodemanager.log-dirs                   yarn:hadoop     drwxr-xr-x
    local       container-executor                          root:hadoop     --Sr-s--*
    local       conf/container-executor.cfg                 root:hadoop     r-------*
    hdfs        /                                           hdfs:hadoop     drwxr-xr-x
    hdfs        /tmp                                        hdfs:hadoop     drwxrwxrwxt
    hdfs        /user                                       hdfs:hadoop     drwxr-xr-x
    hdfs        yarn.nodemanager.remote-app-log-dir         yarn:hadoop     drwxrwxrwxt
    hdfs        mapreduce.jobhistory.intermediate-done-dir  mapred:hadoop   drwxrwxrwxt
    hdfs        mapreduce.jobhistory.done-dir               mapred:hadoop   drwxr-x---

Install  
On master

    mkdir -p /home/hadoop/{hdfs,hdfs/data,hdfs/name}
    groupadd hadoop
    useradd -g hadoop -s /bin/bash -d /home/hdfs -m hdfs
    mkdir /etc/hadoop
    cp core-site.xml,hdfs-site.xml,yarn-site.xml,mapred-site.xml /etc/hadoop 
    su hdfs
    download hadoop-2.7.1.tar.gz
    tar zxvf hadoop-2.7.1.tar.gz -c /usr/local/hadoop
    mkdir logs
    mkdir pid
    cd /usr/local/hadoop
    ./bin/hdfs namenode -format
    ./sbin/hadoop-daemon.sh --config /etc/hadoop/ --script hdfs start namenode
    jps

On slave1,slave2

    useradd -g hadoop -s /bin/bash -d /home/hdfs -m hdfs
    useradd -g hadoop -s /bin/bash -d /home/yarn -m yarn
    mkdir /etc/hadoop
    cp core-site.xml,hdfs-site.xml,yarn-site.xml,mapred-site.xml /etc/hadoop 
    su hdfs
    download hadoop-2.7.1.tar.gz
    tar zxvf hadoop-2.7.1.tar.gz -c /usr/local/hadoop
    mkdir logs
    ./bin/hdfs namenode -format
    ./sbin/hadoop-daemon.sh --config /etc/hadoop/ --script hdfs start datanode
    jps
    exit
    su yarn
    ./sbin/yarn-daemon.sh --config /etc/hadoop/ start nodemanager

On RM 

    useradd -g hadoop -s /bin/bash -d /home/yarn -m yarn
    useradd -g hadoop -s /bin/bash -d /home/mapred -m mapred
    mkdir /etc/hadoop
    cp core-site.xml,hdfs-site.xml,yarn-site.xml,mapred-site.xml /etc/hadoop 
    su hdfs
    download hadoop-2.7.1.tar.gz
    tar zxvf hadoop-2.7.1.tar.gz -c /usr/local/hadoop
    cd /usr/local/hadoop
    mkdir logs
    chmod 774 logs
    ./sbin/yarn-daemon.sh --config /etc/hadoop/ start resourcemanager
    ./sbin/yarn-daemon.sh --config /etc/hadoop/ start proxyserver
    exit
    su mapred
    ./sbin/mr-jobhistory-daemon.sh --config /etc/hadoop/ start historyserver

Web Interfaces

    Daemon                          Web Interface           Notes
    NameNode                        http://nn_host:port/    Default HTTP port is 50070.
    ResourceManager                 http://rm_host:port/    Default HTTP port is 8088.
    MapReduce JobHistory Server     http://jhs_host:port/   Default HTTP port is 19888. 

Execution

On master

    su hdfs
    ./bin/hadoop fs -ls /
    ./bin/hdfs dfs -mkdir /user
    ./bin/hdfs dfs -mkdir /user/hdfs
    ./bin/hdfs dfs -put /etc/hadoop/* input
    ./bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.1.jar grep input output 'dfs[a-z.]+'
    ./bin/hdfs dfs -get output output
    cat output/*
    ./bin/hdfs dfs -cat output/*
