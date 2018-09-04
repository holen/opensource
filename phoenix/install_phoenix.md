# hbase 的查询工具 -- Phoenix
## 简介
Phoenix 是 HBase 的开源 SQL 查询工具。您可以使用标准的 JDBC api，而不是常规的 HBase 客户端 api 来创建表、插入数据和查询 HBase 数据。

现有hbase的查询工具有很多如：Hive，Tez，Impala，Shark/Spark，Phoenix 等。今天主要记录 Phoenix。

phoenix，中文译为“凤凰”，很美的名字。Phoenix 是由 saleforce.com 开源的一个项目，后又捐给了 Apache 基金会。它相当于一个 Java 中间件，提供 jdbc 连接，操作 hbase 数据表。

但是在生产环境中，不可以用在 OLTP 中。在线事务处理的环境中，需要低延迟，而 Phoenix 在查询 HBase 时，虽然做了一些优化，但延迟还是不小。所以依然是用在OLAT中，再将结果返回存储下来。

## 前提条件
- 安装有伪分布式或者分布式的 `HBase 1.2.6` 版本
- 已设置 `HADOOP_HOME`、`HBASE_HOME` 环境变量 
```
    export HADOOP_HOME="/home/hadoop"
    export HBASE_HOME="/home/hbase"
```

## 安装 Phoenix
下载 apache-phoenix-4.13.1-HBase-1.2 版，phoenix-4.13.1 支持 HBase-1.2.6 ，版本要选兼容的，不然问题很多，坑也很多。建议跟着文档的版本来

    wget http://archive.apache.org/dist/phoenix/apache-phoenix-4.13.1-HBase-1.2/bin/apache-phoenix-4.13.1-HBase-1.2-bin.tar.gz
    tar zxvf apache-phoenix-4.13.1-HBase-1.2.tar.gz 
    mv apache-phoenix-4.13.1-HBase-1.2 /home/phoenix
    cd /home/phoenix
    
配置 Phoenix

- 将 `phoenix/` 目录下 `phoenix-core-4.13.1-HBase-1.2.jar`、`phoenix-4.13.1-HBase-1.2-server.jar`、`phoenix-4.13.1-HBase-1.2-client.jar` 拷贝到各个 hbase 的 lib 目录下。
```    
    cp phoenix-core-4.13.1-HBase-1.2.jar /home/hbase/lib/
    cp phoenix-4.13.1-HBase-1.2-server.jar /home/hbase/lib/
    cp phoenix-4.13.1-HBase-1.2-client.jar /home/hbase/lib/
```
- 将 hbase 的配置文件 `hbase-site.xml`、 Hadoop/etc/hadoop 下的 `core-site.xml` 、`hdfs-site.xml` 放到 `phoenix/bin/` 下，替换 Phoenix 原来的配置文件。
```
    cp /home/hbase/conf/hbase-site.xml /home/phoenix/bin/
    cp /home/hadoop/etc/hadoop/core-site.xml /home/phoenix/bin/
    cp /home/hadoop/etc/hadoop/hdfs-site.xml /home/phoenix/bin/
```

- 重启 hbase 集群，使 Phoenix 的 jar 包生效。
```
/home/hbase/bin/stop-hbase.sh
/home/hbase/bin/start-hbase.sh
```

## 验证测试
在 HBase 上生成测试数据，这里我们直接用上篇文章介绍的 Sqoop 把 Mysql 的数据导入到 HBase 中 
```
/home/sqoop/bin/sqoop import --connect jdbc:mysql://192.168.120.201/dev?zeroDateTimeBehavior=round --table agents_role --username abc --password abc123 --hbase-table agents_role --hbase-create-table --column-family cf --hbase-row-key id -m 2 
```
在 HBase shell 上查看导入的数据

    hbase(main):054:0> list   ## 查看 agents_role 表是否存在
    hbase(main):053:0> scan "agents_role"   ## 全表扫描 agents_role 数据
    hbase(main):055:0> get "agents_role", "1"
    COLUMN                                          CELL           
    cf:data                                        timestamp=1536028493764, value=35,30,29,2,6,5,4,3,33,10,9,8,22,13,12,16,15,18,20,21,34,28,27,26,25,24   
    cf:del                                         timestamp=1536028493764, value=0  
    cf:name                                        timestamp=1536028493764, value=\xE4\xB8\x9A\xE5\x8A\xA1\xE8\xB4\x9F\xE8\xB4\xA3\xE4\xBA\xBA                
    cf:type                                        timestamp=1536028493764, value=1  
    cf:updated_at                                  timestamp=1536028493764, value=1535962511                               
    6 row(s) in 0.0290 seconds
    
在 Phoenix 上创建相应的表结构数据，编辑 `agents_role.sql` 文件。  
注意，表名 列名 都要用 "" 双引号引起来，不然会变成大写，例子中 "cf" 为列簇名，需跟 HBase 里的一样。
```
CREATE TABLE IF NOT EXISTS "agents_role" 
(
"id" VARCHAR PRIMARY KEY,
"cf"."name" VARCHAR,
"cf"."type" VARCHAR,
"cf"."data" VARCHAR,
"cf"."del" VARCHAR,
"cf"."updated_at" VARCHAR
);
```
利用 `bin/psql.py` 脚本在 Phoenix 上执行上面的 sql 语句

    ./bin/psql.py 127.0.0.1:2181 agents_role.sql
    
120.0.0.1:2181 为 HBase 的 zookeeper 的访问地址
    
使用 bin 目录下的 `sqlline.py` 脚本登录 Phoenix 进行 sql 查询 HBase 数据

    ./bin/sqlline.py 127.0.0.1:2181
    0: jdbc:phoenix:127.0.0.1:2181> !tables
    0: jdbc:phoenix:127.0.0.1:2181> select * from "agents_role";
    
## Phoenix 常用相关命令
登录命令

    ./sqlline.py localhost:2181
    
帮助

    0: jdbc:phoenix:127.0.0.1:2181> help
    
列出metadata信息

    0: jdbc:phoenix:127.0.0.1:2181> !dbinfo
    
查看当前库中存在的表

    0: jdbc:phoenix:127.0.0.1:2181> !table
    
删除表

    0: jdbc:phoenix:127.0.0.1:2181> drop table "agents_role";
    
查看表结构

    0: jdbc:phoenix:127.0.0.1:2181> !describe "agents_role"
    
退出

    0: jdbc:phoenix:127.0.0.1:2181> !quit
    
## 参考文献
[Phoenix in 15 minutes or less](https://phoenix.apache.org/Phoenix-in-15-minutes-or-less.html)  
[Phoenix Command](https://phoenix.apache.org/language/index.html)  
[Phoenix Install](https://phoenix.apache.org/installation.html#SQL_Client)  
