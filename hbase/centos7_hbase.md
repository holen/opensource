# 在 centos7 安装 hbase2.0 
通过这篇文章，你将会在一个单一节点上运行单机模式和伪分布模式的 Hbase 实例

## 单机模式部署
接下来将描述如何安装单机模式的 hbase 。一个单机实例拥有 Hbase 的所有进程服务： Master、RegionServers 和 Zookeeper 。
### 必需软件安装
hbase 需要 jdk 的支持。故先安装 Java 
### 安装
下载 hbase2.0

    wget http://mirror.bit.edu.cn/apache/hbase/2.0.1/hbase-2.0.1-bin.tar.gz
    tar zxvf hbase-2.0.1-bin.tar.gz
    mv hbase-2.0.1-bin hbase
    cd hbase
    
配置环境变量  
conf/hbase-env.sh

    export JAVA_HOME=/home/jdk1.8.0_141
    
conf/hbase-site.xml 

    <configuration>
      <property>
        <name>hbase.rootdir</name>
        <value>file:///home/testuser/hbase</value>
      </property>
      <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/home/testuser/zookeeper</value>
      </property>
      <property>
        <name>hbase.unsafe.stream.capability.enforce</name>
        <value>false</value>
        <description>
          Controls whether HBase will check for stream capabilities (hflush/hsync).
          Disable this if you intend to run on LocalFileSystem, denoted by a rootdir
          with the 'file://' scheme, but be mindful of the NOTE below.
          WARNING: Setting this to false blinds you to potential data loss and
          inconsistent system state in the event of process and/or node failures. If
          HBase is complaining of an inability to use hsync or hflush it's most
          likely not a false positive.
        </description>
      </property>
    </configuration>

参数说明

    hbase.rootdir 设置 hbase 在本地文件系统的存储目录
    hbase.zookeeper.property.dataDir 设置 zookeeper 在本地文件系统的存储目录
    hbase.unsafe.stream.capability.enforce 单机部署设置为 false 
    
启动 hbase

    bin/start-hbase.sh
    
使用 jps 就可以查看到 hbase 开启的相应进程。如 HMaster、HRegionServer 和 HQuorumPeer  
使用 http://192.168.120.202:16010 查看 HBase Web UI

### 相关操作命令
连接到 hbase 

    ./bin/hbase shell
    
显示帮助

    hbase(main):001:0> help
    
创建表
    
    hbase(main):001:0> create 'test', 'cf'
    
列出表信息

    hbase(main):002:0> list 'test'
    
列出详细表信息

    hbase(main):003:0> describe 'test'
    
插入表数据
    
    hbase(main):004:0> put 'test', 'row1', 'cf:a', 'value1'
    
查看表数据

    hbase(main):005:0> scan 'test'
    
禁用/启用表

    hbase(main):008:0> disable 'test'
    hbase(main):009:0> enable 'test'
    
删除表

    hbase(main):011:0> drop 'test'
    
退出

    exit
    
## 伪分布式部署
先关掉单机实例进程

    $ ./bin/stop-hbase.sh

配置 hbase-site.xml 

    <configuration>
        <property>
          <name>hbase.cluster.distributed</name>
          <value>true</value>
        </property>
        <property>
          <name>hbase.rootdir</name>
          <value>hdfs://192.168.120.202:9000/hbase</value>
        </property>
        <property>
            <name>hbase.unsafe.stream.capability.enforce</name>
            <value>false</value>
            <description>
            </description>
        </property>
        <property>
          <name>hbase.zookeeper.quorum</name>
          <value>192.168.120.202</value>
        </property>
        <property>
          <name>hbase.zookeeper.property.dataDir</name>
          <value>/home/hbase/zookeeper/data</value>
        </property>
        <property>
            <name>zookeeper.session.timeout</name>
            <value>90000</value>
        </property>
    </configuration>
    
参数说明

    hbase.cluster.distributed 设置 hbase 模式为 分布式 模式
    hbase.rootdir 更改存储目录为 hdfs 的目录
    hbase.zookeeper.quorum 设置 zookeeper 节点
    hbase.zookeeper.property.dataDir 设置 zookeeper 存储目录
    zookeeper.session.timeout 设置超时时间

启动 hbase 

    bin/start-hbase.sh
    
jps 显示

    31506 HRegionServer
    31352 HMaster
    31215 HQuorumPeer
    
检查 HBase 目录是否存在于 HDFS

    $ /home/hadoop/bin/hadoop fs -ls /hbase
    
停止 hbase

    $ ./bin/stop-hbase.sh
