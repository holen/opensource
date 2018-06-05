# install phoenix for CDH5.14.2
Ref: https://www.jianshu.com/p/9d3e938081d2
Ref: http://phoenix.apache.org/Phoenix-in-15-minutes-or-less.html

download phoenix

    wget https://mirrors.tuna.tsinghua.edu.cn/apache/phoenix/apache-phoenix-4.13.2-cdh5.11.2/bin/apache-phoenix-4.13.2-cdh5.11.2-bin.tar.gz

copy jar to Hbase lib on all RegionServer node

    tar zxvf apache-phoenix-4.13.2-cdh5.11.2-bin.tar.gz
    cd apache-phoenix-4.13.2-cdh5.11.2-bin
    cp phoenix-4.13.2-cdh5.11.2-server.jar /opt/cloudera/parcels/CDH-5.14.2-1.cdh5.14.2.p0.3/lib/hbase/lib/
    cp phoenix-core-4.13.2-cdh5.11.2.jar /opt/cloudera/parcels/CDH-5.14.2-1.cdh5.14.2.p0.3/lib/hbase/lib/

增加hbase-site.xml 配置  
Hbase->配置->高级->hbase-site.xml

    <property>
    <name>hbase.table.sanity.checks</name>
    <value>false</value>
    </property>

restart hbase

login phoenix

    ./bin/sqlline.py 192.168.120.202:2181
    help
    !tables
    !quit

Test import some data

    ./bin/psql.py 192.168.120.202:2181 us_population.sql us_population.csv us_population_queries.sql 
