查看哪个结点被选作leader或者follower
echo stat|nc 127.0.0.1 2181

root@ubuntu:/usr/lib/zookeeper/bin# echo stat|nc 127.0.0.1 2181 
Zookeeper version: 3.4.5-cdh4.4.0--1, built on 09/04/2013 01:46 GMT
Clients:
 /127.0.0.1:57736[0](queued=0,recved=1,sent=0)


Latency min/avg/max: 0/0/0
Received: 1
Sent: 0
Connections: 1
Outstanding: 0
Zxid: 0x0
Mode: standalone
Node count: 4

查看具体结点信息
bash zkServer.sh status

erver，若回复imok表示已经启动
echo ruok|nc 127.0.0.1 2181

    1. 以通过命令：echo stat|nc 127.0.0.1 2181 来查看哪个节点被选择作为follower或者leader
    2. 使用echo ruok|nc 127.0.0.1 2181 测试是否启动了该Server，若回复imok表示已经启动。
    3. echo dump| nc 127.0.0.1 2181 ,列出未经处理的会话和临时节点。
    4. echo kill | nc 127.0.0.1 2181 ,关掉server
    5. echo conf | nc 127.0.0.1 2181 ,输出相关服务配置的详细信息。
    6. echo cons | nc 127.0.0.1 2181 ,列出所有连接到服务器的客户端的完全的连接 / 会话的详细信息。
    7. echo envi |nc 127.0.0.1 2181 ,输出关于服务环境的详细信息（区别于 conf 命令）。
    8. echo reqs | nc 127.0.0.1 2181 ,列出未经处理的请求。
    9. echo wchs | nc 127.0.0.1 2181 ,列出服务器 watch 的详细信息。
    10. echo wchc | nc 127.0.0.1 2181 ,通过 session 列出服务器 watch 的详细信息，它的输出是一个与 watch 相关的会话的列表。
    11. echo wchp | nc 127.0.0.1 2181 ,通过路径列出服务器 watch 的详细信息。它输出一个与 session 相关的路径。

连接到zookeeper
./zookeeper-shell.sh 127.0.0.1:2181
输入help显示帮助信息

使用 ls 命令来查看当前 ZooKeeper 中所包含的内容：
[zk: 202.115.36.251:2181(CONNECTED) 1] ls /
[zookeeper]

创建一个新的 znode ，使用 create /zk myData 。这个命令创建了一个新的 znode 节点“ zk ”以及与它关联的字符串：
[zk: 202.115.36.251:2181(CONNECTED) 2] create /zk "myData"
Created /zk 

我们运行 get 命令来确认 znode 是否包含我们所创建的字符串
[zk: 202.115.36.251:2181(CONNECTED) 3] get /zk
cZxid = 0x6
ctime = Thu Sep 12 15:49:16 CST 2013
mZxid = 0x7
mtime = Thu Sep 12 15:49:38 CST 2013
pZxid = 0x6
cversion = 0
dataVersion = 1
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 10
numChildren = 0

下面我们通过 set 命令来对 zk 所关联的字符串进行设置
[zk: 202.115.36.251:2181(CONNECTED) 4] set /zk "zsl"
"myData"
cZxid = 0x4
ctime = Thu Sep 12 15:46:37 CST 2013
mZxid = 0x4
mtime = Thu Sep 12 15:46:37 CST 2013
pZxid = 0x4
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 8
numChildren = 0

下面我们将刚才创建的 znode 删除：
[zk: 202.115.36.251:2181(CONNECTED) 5] delete /zk


