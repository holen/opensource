# Backup and restore (slave)
Backup

    mongodump -d test -o backup
    
restore

    mongorestore -d foo --drop backup/test
    
fsync and lock

    fsync 命令会强制服务器将所有缓冲区写入磁盘
    root@logstash:~# mongo
    MongoDB shell version: 2.6.0
    connecting to: test
    > use admin
    switched to db admin
    > db.runCommand({"fsync":1, "lock":1});
    {
            "info" : "now locked against writes, use db.fsyncUnlock() to unlock"            ,
            "seeAlso" : "http://dochub.mongodb.org/core/fsynccommand",
            "ok" : 1
    }
 
修复未正常停止MongoDB数据库

    mongod --repair
    > use test
    switched to db test
    > db.repairDatabase() 
    

