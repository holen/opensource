# Install hadoop on Centos7
ref: http://hadoop.apache.org/docs/r2.9.1/hadoop-project-dist/hadoop-common/ClusterSetup.html

## Prerequisites
Setup env  

1. Master服务必须可以无密码登录Slave

2. /etc/profile

    # java path
    JAVA_HOME=/home/jdk1.8.0_141
    JRE_HOME=$JAVA_HOME/jre
    PATH=$PATH:$JAVA_HOME/bin
    CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
    export JAVA_HOME
    export JRE_HOME
    export PATH
    export CLASSPATH

    HADOOP_PREFIX=/home/hadoop
    export HADOOP_PREFIX

    HADOOP_CONF_DIR=/home/hadoop/etc/hadoop
    export HADOOP_CONF_DIR

Configure xml file

    mkdir /home/hadoop/hdfs/{data,name}
    etc/hadoop/core-site.xml, etc/hadoop/hdfs-site.xml, etc/hadoop/yarn-site.xml and etc/hadoop/mapred-site.xml
    etc/hadoop/slave

## Hadoop Startup
    
    ./bin/hdfs namenode -format
    ./sbin/start-dfs.sh
    ./sbin/start-yarn.sh
    ./sbin/mr-jobhistory-daemon.sh --config $HADOOP_CONF_DIR start historyserver
    /home/hadoop/bin/hadoop fs -ls /

To start a Hadoop cluster you will need to start both the HDFS and YARN cluster.

The first time you bring up HDFS, it must be formatted. Format a new distributed filesystem as hdfs:

    [hdfs]$ $HADOOP_PREFIX/bin/hdfs namenode -format <cluster_name>

Start the HDFS NameNode with the following command on the designated node as hdfs:

    [hdfs]$ $HADOOP_PREFIX/sbin/hadoop-daemon.sh --config $HADOOP_CONF_DIR --script hdfs start namenode

Start a HDFS DataNode with the following command on each designated node as hdfs:

    [hdfs]$ $HADOOP_PREFIX/sbin/hadoop-daemons.sh --config $HADOOP_CONF_DIR --script hdfs start datanode

If etc/hadoop/slaves and ssh trusted access is configured (see Single Node Setup), all of the HDFS processes can be started with a utility script. As hdfs:

    [hdfs]$ $HADOOP_PREFIX/sbin/start-dfs.sh

Start the YARN with the following command, run on the designated ResourceManager as yarn:

    [yarn]$ $HADOOP_YARN_HOME/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR start resourcemanager

Run a script to start a NodeManager on each designated host as yarn:

    [yarn]$ $HADOOP_YARN_HOME/sbin/yarn-daemons.sh --config $HADOOP_CONF_DIR start nodemanager

Start a standalone WebAppProxy server. Run on the WebAppProxy server as yarn. If multiple servers are used with load balancing it should be run on each of them:

    [yarn]$ $HADOOP_YARN_HOME/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR start proxyserver

If etc/hadoop/slaves and ssh trusted access is configured (see Single Node Setup), all of the YARN processes can be started with a utility script. As yarn:

    [yarn]$ $HADOOP_PREFIX/sbin/start-yarn.sh

Start the MapReduce JobHistory Server with the following command, run on the designated server as mapred:

    [mapred]$ $HADOOP_PREFIX/sbin/mr-jobhistory-daemon.sh --config $HADOOP_CONF_DIR start historyserver

## Hadoop Shutdown

Stop the NameNode with the following command, run on the designated NameNode as hdfs:

    [hdfs]$ $HADOOP_PREFIX/sbin/hadoop-daemon.sh --config $HADOOP_CONF_DIR --script hdfs stop namenode

Run a script to stop a DataNode as hdfs:

    [hdfs]$ $HADOOP_PREFIX/sbin/hadoop-daemons.sh --config $HADOOP_CONF_DIR --script hdfs stop datanode

If etc/hadoop/slaves and ssh trusted access is configured (see Single Node Setup), all of the HDFS processes may be stopped with a utility script. As hdfs:

    [hdfs]$ $HADOOP_PREFIX/sbin/stop-dfs.sh

Stop the ResourceManager with the following command, run on the designated ResourceManager as yarn:

    [yarn]$ $HADOOP_YARN_HOME/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR stop resourcemanager

Run a script to stop a NodeManager on a slave as yarn:

    [yarn]$ $HADOOP_YARN_HOME/sbin/yarn-daemons.sh --config $HADOOP_CONF_DIR stop nodemanager

If etc/hadoop/slaves and ssh trusted access is configured (see Single Node Setup), all of the YARN processes can be stopped with a utility script. As yarn:

    [yarn]$ $HADOOP_PREFIX/sbin/stop-yarn.sh

Stop the WebAppProxy server. Run on the WebAppProxy server as yarn. If multiple servers are used with load balancing it should be run on each of them:

    [yarn]$ $HADOOP_YARN_HOME/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR stop proxyserver

Stop the MapReduce JobHistory Server with the following command, run on the designated server as mapred:

    [mapred]$ $HADOOP_PREFIX/sbin/mr-jobhistory-daemon.sh --config $HADOOP_CONF_DIR stop historyserver

## Web Interfaces

Once the Hadoop cluster is up and running check the web-ui of the components as described below:

    Daemon  Web Interface   Notes
    NameNode    http://nn_host:port/    Default HTTP port is 50070.
    ResourceManager     http://rm_host:port/    Default HTTP port is 8088.
    MapReduce JobHistory Server     http://jhs_host:port/   Default HTTP port is 19888. 

