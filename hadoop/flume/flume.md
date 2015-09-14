# Flume 
Install 

    apt-get install openjdk-7-jdk
    wget http://mirror.bit.edu.cn/apache/flume/1.6.0/apache-flume-1.6.0-bin.tar.gz
    tar zxvf apache-flume-1.6.0-bin.tar.gz
    cd apache-flume-1.6.0-bin/
    cp conf/flume-env.sh.template conf/flume-env.sh

    vim conf/flume-env.sh
    export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64

    ./bin/flume-ng version

Execute

    ./bin/flume-ng agent --conf conf --conf-file example.conf --name a1 -Dflume.root.logger=INFO,console
    
On another term

    telnet localhost 44444

Flume + kafka + storm 架构

    1）数据采集
    负责从各节点上实时采集数据，选用cloudera的flume来实现
    2）数据接入
    由于采集数据的速度和数据处理的速度不一定同步，因此添加一个消息中间件来作为缓冲，选用apache的kafka
    3）流式计算
    对采集到的数据进行实时分析，选用apache的storm
    4）数据输出
    对分析后的结果持久化，暂定用mysql

![架构图](http://www.aboutyun.com/data/attachment/forum/201402/10/150105etbwmjcaoexcbta7.jpg)
