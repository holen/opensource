# mongodb replication
master

    mkdir /data/master 
    mongod --dbpath /data/master --port 10000 --master >> /var/log/mongo.log & 
    
slave 
    
    mkdir /data/slave
    mongod --dbpath /data/slave --port 10001 --slave --source localhost:10000 >> /var/log/mongo-slave.log & 
    
other option

    --only  # specified database
    --slavedelay # 从节点延迟
    --fastsync # 以主节点的数据快照为基础启动从节点
    --autoresync # 自动同步
    --oplogSize # log size
    
mongodb client

    mongo --port 10000 
    > use local
    > db.sources.insert({"host": "localhost:27017"})
    > db.sources.find()
    > db.sources.remove({"host":"localhost:27017"})
    
# Replica Set
start mongodb instance

    mkdir -p /data/node1 /data/node2
    mongod --dbpath /data/node1 --port 10001 --replSet rs1 
    mongod --dbpath /data/node2 --port 10002 --replSet rs1 
    
initiate
    
    mongodb 127.0.0.1:10001
    > config = {_id:"rs1",members:[{_id:0,host:"127.0.0.1:10001"},{_id:1,host:"127.0.0.1:10002"}]} 
    > rs.initiate(config)
    > rs.status()
    > use mydb
    > db.users.find()
    > show dbs
    > rs.conf()
    > db.isMaster() 
    > rs.reconfig() --> overwrites the existing replica set configuration 
    
    mongodb 127.0.0.1:10002 --> second
    > db.user.find()  --> false
    > rs.slaveOk()
    > db.users.find()
    > use mydb
    > db.users.find()
    > db.user.insert({name:"jack"})  --> false
    
add another instance

    mkdir -p /data/node3
    mongod --dbpath /data/node3 --port 10003 --replSet rs1
    rs.add("127.0.0.1:10003")
    rs.status()

Check replica status

    master: db.printReplicationInfo()

节点类型

    standard --> 能成为活动节点
    passive  --> 不能成为活动节点 priority = 0
    arbiter  --> 仲裁者

Adjust priority --> 由大到小

    mongodb 127.0.0.1:10001 
    > cfg = rs.conf()
    > cfg.members[0].priority = 0.5
    > cfg.members[1].priority = 2
    > cfg.members[2].priority = 2
    > rs.reconfig(cfg)

end

    must have three-member replica set from three existing mongod instances 
    3个Standard节点组成Replication Sets是可以的,当PRIMARY节点DOWN了还是可以再选出一个PRIMARY节点,此时要马上修复DOWN机的节点,因为不修复的话如果当前的PRIMARY节点再DOWN了,剩下一个SECONDARY节点是不能选出PRIMARY节点的! 
 
参考文献

[Deploy a Replica Set for Testing and Development](http://docs.mongodb.org/manual/tutorial/deploy-replica-set-for-testing/)  
[MongoDB副本集replSet配置与分析](http://blog.csdn.net/irelandken/article/details/8003315)
