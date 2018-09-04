# 在 centos7 上安装 Hadoop
这是一篇 hadoop 的安装与配置教程。通过这篇教程，我们将会安装一个单机 hadoop ，以便于我们能更快更简单的操作 hadoop MapReduce 。
## 安装前需要准备的软件
Centos7 下必备软件

- Java 必需要安装
- ssh 必需安装

## 下载 hadoop2.7 版本

    wget http://mirrors.shu.edu.cn/apache/hadoop/common/hadoop-2.7.6/hadoop-2.7.6.tar.gz
    tar zxvf hadoop-2.7.6.tar.gz
    cd hadoop-2.7.6

## 设置环境变量
编辑 etc/hadoop/hadoop-env.sh 文件，设置 JAVA_HOME 变量

    export JAVA_HOME="/home/jdk1.8.0_141"

试运行如下命令

    bin/hadoop
    
譔脚本将会显示 hadoop 脚本的使用文档

## 单机模式
默认情况下， Hadoop 处理单机运行模式，运行在单个 java 进程。这样可以更好的用于调试。  
下面只是一个简单的例子，复制配置文件到 hadoop 的 input 目录里，统计匹配到的字词，结果输出到 output

    $ mkdir input
    $ cp etc/hadoop/*.xml input
    $ bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.9.1.jar grep input output 'dfs[a-z.]+'
    $ cat output/*
    
## 伪分布模式
Hadoop 也可以运行在单一节点的伪分布模式下，也是运行在单个 Java 进程上。  
### 配置
etc/hadoop/core-site.xml:

    <configuration>
        <property>
            <name>fs.defaultFS</name>
            <value>hdfs://192.168.120.202:9000</value>
        </property>
    </configuration>
    
etc/hadoop/hdfs-site.xml:

    <configuration>
        <property>
            <name>dfs.replication</name>
            <value>1</value>
        </property>
        <property>
            <name>dfs.namenode.name.dir</name>
            <value>file:/home/hadoop/hdfs/name</value>
        </property>
        <property>
            <name>dfs.datanode.data.dir</name>
            <value>/home/hadoop/hdfs/data</value>
        </property>
    </configuration>
    
### 设置免密码登录
检测是否可以免密码登录

    $ ssh localhost
    
如果不能，则

    $ ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
    $ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    $ chmod 0600 ~/.ssh/authorized_keys
    
### 执行命令
下面将介绍在本地 hadoop 上运行一个 MapReduce 任务

先格式化文件系统

    $ bin/hdfs namenode -format
    
启动 NameNode 和 DataNode 进程

    $ bin/hdfs namenode -format
    
Hadoop 程序日志都放在 $HADOOP\_LOG\_DIR 目录 (默认是 $HADOOP_HOME/logs)  
通过浏览器访问 NameNode 的 web 接口

    NameNode - http://192.168.120.202:50070/

创建 HDFS 目录

    $ bin/hdfs dfs -mkdir -p /user/root/input
    
复制 etc/hadoop 下的配置文件到 hadoop 文件系统的 input 目录下

    $ bin/hdfs dfs -put etc/hadoop/* /user/root/input/
    
运行测试例子

    $ bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.6.jar grep input output 'dfs[a-z.]+'
    
检查结果: 从 hadoop 文件系统的 output 目录下的文件复制到本地文件系统的 output 目录，并查看结果

    $ bin/hdfs dfs -get output output
    $ cat output/*
    
也可以直接从 hadoop 文件系统上查看 

    $ bin/hdfs dfs -cat output/*
    
关闭 hadoop 进程 

    $ sbin/stop-dfs.sh
    
### 在伪分布模式下使用 YARN
我们可以在伪分布模式下通过 YARN 运行一个 MapReduce 任务，只要通过一个参数配置和开启 ResourceManager 与 NodeManager 进程  
配置参数 etc/hadoop/mapred-site.xml：

    <configuration>
        <property>
            <name>mapreduce.framework.name</name>
            <value>yarn</value>
        </property>
    </configuration>
    
etc/hadoop/yarn-site.xml:

    <configuration>
        <property>
            <name>yarn.nodemanager.aux-services</name>
            <value>mapreduce_shuffle</value>
        </property>
    </configuration>
    
启动 ResourceManager 与 NodeManager 进程

    $ sbin/start-yarn.sh
    
可以在浏览器上访问 ResourceManager 的 web 接口

    ResourceManager - http://192.168.120.202:8088/
    
停止运行

    $ sbin/stop-yarn.sh

## HDFS 中 dfs 的一些常用命令
查看帮助

    bin/hdfs dfs -help

创建一个文件夹

    bin/hdfs dfs -mkdir /test

将本地文件上传到 hdfs 中

    bin/hdfs dfs -put 10.txt /test/

列出路径下的所有文件和文件夹

    bin/hdfs dfs -ls /test/

查看文件中的内容

    bin/hdfs dfs -cat /test/10.txt

列出文件中的内容

    bin/hdfs dfs -text /test/10.txt

创建一个空文件

    bin/hdfs dfs -touchz /textFile

递归列出路径下的文件夹和文件

    bin/hdfs dfs -ls -R /

将文件从A 移动到 B

    bin/hdfs dfs -mv /test/10.txt /test

将 A 处的文件 复制一份到 B处

    bin/hdfs dfs -cp /test/10.txt /

将文件从本地移动到 hdfs 系统中(本地文件会被删除)

    bin/hdfs dfs -moveFromLocal /home/bigdata/eclipse/testFile/Reduced/C000008/100.txt /test

删除文件

    bin/hdfs dfs -rm /test/100.txt

删除文件夹

    bin/hdfs dfs -rmdir /test/testDir

将文件从 hdfs 系统移动到本地文件系统

    bin/hdfs dfs -get /test/testFile /home/
    
## 参考文献
[Hadoop: Setting up a Single Node Cluster](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SingleCluster.html)
