# Sharding
说明

    Sharding is a method for storing data across multiple machines. 
    MongoDB分片的基本思想就是将集合切分成小块，这些小块分散到诺干片里面，每个片只负责总数据的一部分

应用情景

    磁盘不够
    单个mongod已经不能满足写数据的性能要求
    想将大量数据放在内存中提高性能
    
shard keys <==> index 

    启动配置服务器
        mongod --dbpath /data/config --port 2000
    
    启动mongos
        mongos --port 30000 --configdb localhost:2000
    
    添加shard
    
        mongod --dbpath /data/dbs/shard1/ --port 10000  
        root@logstash:/data/dbs# mongo localhost:30000/admin
        MongoDB shell version: 2.6.0
        connecting to: localhost:30000/admin
        mongos> db.runCommand({addshard:"localhost:10000",allowLocal:true})
        { "shardAdded" : "shard0000", "ok" : 1 }
    
    切分数据
    
        开启foo分片
        mongos> db.runCommand({"enablesharding":"foo"})
        { "ok" : 1 }
        
        对集合进行分片
        mongos> db.runCommand({"shardcollection":"foo.bar","key":{"_id":1}})
        { "collectionsharded" : "foo.bar", "ok" : 1 }
 
管理分片

    查找片
    mongos> use config
    switched to db config
    mongos> db.shards.find()
    { "_id" : "shard0000", "host" : "localhost:10000" } 
    
    数据库
    mongos> db.databases.find()
    { "_id" : "admin", "partitioned" : false, "primary" : "config" }
    { "_id" : "foo", "partitioned" : true, "primary" : "shard0000" } 
    
    块
    mongos> db.chunks.find()
    { "_id" : "foo.bar-_id_MinKey", "lastmod" : Timestamp(1, 0), "lastmodEpoch" : ObjectId("5375cfeca8dc76298d19160d"), "ns" : "foo.bar", "min" : { "_id" : { "$minKey" : 1 } }, "max" : { "_id" : { "$maxKey" : 1 } }, "shard" : "shard0000" }
    
    分片命令
    mongos>db.printShardingStatus()
    mongos>db.runCommand({"removeshard":"localhost:10000"});

