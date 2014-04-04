# Install java tomcat6 zookeeper

## Install jdk

    cd /opt/
    chmod +x jdk-6u45-linux-x64.bin
    ./jdk-6u45-linux-x64.bin

    update-alternatives --config java

    echo '
    #set java environment  
    JAVA_HOME=/opt/jdk1.6.0_45
    export JRE_HOME=/opt/jdk1.6.0_45/jre
    export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH  
    export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH ' >> /etc/profile
    source /etc/profile

## Install tomcat6

    wget http://mirrors.cnnic.cn/apache/tomcat/tomcat-6/v6.0.39/bin/apache-tomcat-6.0.39.tar.gz 
    tar zxvf apache-tomcat-6.0.37.tar.gz
    /opt/apache-tomcat-6.0.37/bin/startup.sh 

    echo '
    ## tomcat environment
    export CATALINA_HOME=/opt/apache-tomcat-6.0.37 ' >> /etc/profile
    source /etc/profile 

    vim catalina.sh , 找到
    # OS specific support. $var _must_ be set to either true or false.
    在这行上面再定义一次CATALINA_HOME以及JAVA_HOME：
    CATALINA_HOME=/opt/apache-tomcat-6.0.37
    JAVA_HOME=/opt/jdk1.6.0_45

run as service 

    ln -s /opt/apache-tomcat-6.0.37/bin/catalina.sh /etc/init.d/tomcat
    servcie tomcat status
    update-rc.d –f tomcat defaults

## Install zookeeper

    wget http://mirrors.hust.edu.cn/apache/zookeeper/zookeeper-3.4.5/zookeeper-3.4.5.tar.gz
    tar zxvf zookeeper-3.4.5.tar.gz
    cp zookeeper-3.4.5/conf/zoo_sample.cfg zookeeper-3.4.5/conf/zoo.cfg

