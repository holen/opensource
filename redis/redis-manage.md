# Redis manage

## 持久化

RDB方式（默认）:通过快照完成 （可备份RDB文件）


    save 900 1      # 15分钟(900s)内有至少一个键被更改则进行快照
    save 300 10
    save 60 1000
    dbfilename dump.rdb 
    dir /data/redis/6379 
    
    快照过程：
    1）Redis使用fork函数复制一份当前进程（父进程）的副本（子进程）
    2) 父进程继续接收并处理客户端发来的命令，而子进程开始将内存中的数据写入硬盘中的临时文件；
    3) 当子进程写入完所有数据后会用该临时文件替换旧的RDB文件，至此一次快照操作完成
    
AOF（append only file)方式（重启载入比较慢）

    开启
    appendonly yes
    appendfilename appendonly.aof
    auto-aof-rewrite-percentage 100 #当目前的AOF文件大小超过上一次重写时的AOF文件大小的百分之多少时会再次进行重写
    auto-aof-rewrite-mini-size 64mb #允许重写的最小AOF文件大小
    # appendfsync always
    appendsync everysec #每秒执行一次硬盘缓存写入硬盘的同步操作
    # appendfsync no
    
## 复制

master

    redis-server 
    
slave 

    redis-server --slaveof 10.0.0.33 6379
    vim /etc/redis.conf
    slaveof 10.0.0.33 6379 
    redis>slaveof 127.0.0.1 6379
    
## 安全

可信环境

    bind 127.0.0.1
    
数据库密码

    requirepass TAFK(@~!jiXALQ
    
http://www.cnblogs.com/stephen-liu74/archive/2012/04/11/2370521.html
