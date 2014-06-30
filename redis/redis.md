# Redis
Install 

    $ wget http://download.redis.io/releases/redis-2.8.9.tar.gz
    $ tar xzf redis-2.8.9.tar.gz
    $ cd redis-2.8.9
    $ make 
    $ make install
    $ make test

configure 

    $ mkdir /etc/redis/
    $ mkdir -p /data/redis/6379
    $ cp /usr/local/redis-2.8.9/redis.conf /etc/redis/redis.conf
    $ vim /etc/redis/redis.conf
        daemonize   yes             # 使redis以守护进程模式运行
        pidfile /var/run/redis_6379.pid
        port    6379
        dir     /data/redis/6379    # 设置持久化文件存放位置

start 

    $ /etc/init.d/redis start
    
stop

    $ redis-cli shutdown
    
client 

    $ redis-cli -h 127.0.0.1 -p 6379
    $ redis-cli PING
    PONG
    $ redis-cli
    127.0.0.1:6379> ping
    PONG
    127.0.0.1:6379> echo hi
    "hi"
    127.0.0.1:6379> INCR foo
    (integer) 1
    127.0.0.1:6379> GET foo
    "1"
    127.0.0.1:6379> GET noexits
    (nil)
    127.0.0.1:6379> keys * 
    1) "foo"
    127.0.0.1:6379> config set loglevel warning # 动态修改redis.conf配置
    OK      
    127.0.0.1:6379> config get loglevel
    1) "loglevel"
    2) "warning"
    
选择数据库    
    
    127.0.0.1:6379> select 1    
    OK
    127.0.0.1:6379[1]> get foo
    (nil)
    127.0.0.1:6379> set bar 1
    OK
    127.0.0.1:6379> KEYS *
    1) "bar"
    2) "foo"
    
判断键是否存在    
    
    127.0.0.1:6379> EXISTS key 
    (integer) 0
    127.0.0.1:6379> EXISTS bar
    (integer) 1
    
删除键     
    
    127.0.0.1:6379> del bar 
    (integer) 1
    ## also -> redis-cli DEL 'redis-cli KEYS "user:*"'
    127.0.0.1:6379> del bar
    (integer) 0
    127.0.0.1:6379> EXISTS bar
    (integer) 0
    
## 数据类型
    
获取键值的数据类型    
    
    127.0.0.1:6379> TYPE foo 
    string
    127.0.0.1:6379> LPUSH bar 1 #LPUSH 向指定的列表类型键中增加一个元素
    (integer) 1
    127.0.0.1:6379> TYPE bar
    list 
 
递增数字

    127.0.0.1:6379> INCR num
    (integer) 1
    127.0.0.1:6379> INCR num
    (integer) 2
     
键命名

    对象类型：对象ID ：对象属性 
    eg: users:1:friends. 来存储ID为1的用户的好友列表，多个单词用.分隔
    
生成自增ID

    users:count
    INCR users:count
    
存储数据

    每个字符串类型键只能存储一个字符串，so需要序列化函数(PHP的serialize和JavaScript的JSON.stringify)将他们转换成一个字符串
    也可以使用MessagePack进行序列化
    
增加指定的整数

    127.0.0.1:6379> INCRBY num 2
    (integer) 4
    127.0.0.1:6379> INCRBY num 3
    (integer) 7
    
减少指定的整数

    DECR key
    DECRBY key decrement
    
增加指定浮点数

    INCRBYFLOAT key increment
    
向尾部追加值

    APPEND key value
    
    127.0.0.1:6379> set key hello
    OK
    127.0.0.1:6379> APPEND key " world!" #空格需要双引号区分
    (integer) 12
 
获取字符串长度

    127.0.0.1:6379> strlen key
    (integer) 12
    
同时获得/设置多个键值

    127.0.0.1:6379> MSET key1 v1 key2 v2 key3 v3
    OK
    127.0.0.1:6379> GET key2
    "v2"
    127.0.0.1:6379> MGET key1 key3
    1) "v1"
    2) "v3"
 
位操作 -->可以紧凑的存储布尔值（如性别：男性和女性）

    SETBIT key offset value
    BITCOUNT key [start] [end]
    BITOP operation destkey key [key...]
    
## 散列类型

赋值

    HSET key field value
    HGET key field
    HMSET key field value [field value ...]
    HMGET eky field [field ...]
    HGETALL key
    
    127.0.0.1:6379> HSET car price 50000
    (integer) 1
    127.0.0.1:6379> HSET car name BMW
    (integer) 1
    127.0.0.1:6379> HGET car name
    "BMW"
    127.0.0.1:6379> HGET car price
    "50000"
    127.0.0.1:6379> HMGET car price name
    1) "50000"
    2) "BMW"
    127.0.0.1:6379> HGETALL car
    1) "price"
    2) "50000"
    3) "name"
    4) "BMW"
    
判断字段是否存在

    HEXISTS key field
    127.0.0.1:6379> HEXISTS car model
    (integer) 0
    127.0.0.1:6379> HEXISTS car price
    (integer) 1
    
当字段不存在时赋值

    HSETNX key field value
    
增加数字

    HINCRBY key field increment
    
删除字段

    HDEL key field [field ...]
    
只获取字段名或字段值

    HKEYS key
    HVALS key

获取字段数量

    HLEN key

    127.0.0.1:6379> HKEYS car
    1) "price"
    2) "name"
    127.0.0.1:6379> HVALS car
    1) "50000"
    2) "BMW"
    127.0.0.1:6379> HLEN car
    (integer) 2
 
## 列表类型

向列表两端增加元素

    LPUSH key value [value ...]
    RPUSH key value [value ...]
    127.0.0.1:6379> LPUSH numbers 1
    (integer) 1
    127.0.0.1:6379> LPUSH numbers 2 3 
    (integer) 3
    127.0.0.1:6379> RPUSH numbers 0 -1
    (integer) 5

从列表两端弹出元素

    LPOP key # 会移除元素
    RPOP key # 会移除元素
    
获取列表中元素的个数

    LLEN key
    
获取列表片段

    LRANGE key start stop
    127.0.0.1:6379> LRANGE numbers 0 2
    1) "2"
    2) "1"
    3) "0"
    127.0.0.1:6379> LRANGE numbers -2 -1
    1) "1"
    2) "0"
      
删除列表中指定的值

    LREM key count value
    127.0.0.1:6379> RPUSH numbers 2
    (integer) 4
    127.0.0.1:6379> LRANGE numbers 0 -1
    1) "2"
    2) "1"
    3) "0"
    4) "2"
    127.0.0.1:6379> LREM numbers -1 2 
    (integer) 1
    127.0.0.1:6379> LRANGE numbers 0 -1
    1) "2"
    2) "1"
    3) "0"

获得/设置指定索引的元素值

    LINDEX key index
    LSET key index value 
    127.0.0.1:6379> LINDEX numbers 0 
    "2"
    127.0.0.1:6379> LINDEX numbers -1
    "0"
    127.0.0.1:6379> LSET numbers 1 7
    OK
    127.0.0.1:6379> LINDEX numbers 1
    "7"
 
只保留列表指定片段

    LTRIM key start end # LTRIM经常和LPUSH一起使用来限制列表中元素的数量
    127.0.0.1:6379> LRANGE numbers 0 -1
    1) "2"
    2) "7"
    3) "0"
    127.0.0.1:6379> LTRIM numbers 1 2 
    OK
    127.0.0.1:6379> LRANGE numbers 0 -1 
    1) "7"
    2) "0"

向列表中插入元素

    LINSERT key BEFORE|AFTER pivot value 
    127.0.0.1:6379> LRANGE numbers 0 -1 
    1) "7"
    2) "0"
    127.0.0.1:6379> LINSERT numbers AFTER 7 3
    (integer) 3
    127.0.0.1:6379> LRANGE numbers 0 -1
    1) "7"
    2) "3"
    3) "0"
     
将元素从一个列表转到另一个列表R 

    POPLPUSH source destination
    
集合类型

增加/删除元素
    
    SADD key member [member ...]
    SREM key member [member ...]
    127.0.0.1:6379> SADD letters a 
    (integer) 1
    127.0.0.1:6379> SADD letters a b c 
    (integer) 2
    127.0.0.1:6379> SREM letters c d
    (integer) 1
    
获得集合中的所有元素

    SMEMBERS key 
    127.0.0.1:6379> SMEMBERS letters
    1) "b"
    2) "a" 
    
判断元素是否在集合中

    SISMEMBER key member
    127.0.0.1:6379> SISMEMBER letters a 
    (integer) 1
    127.0.0.1:6379> SISMEMBER letters d
    (integer) 0 
    
集合间运算

    SDIFF key [key ...] # 差集
    SINTER key [key ...] # 交集
    SUNION key [key ...] # 并集
    127.0.0.1:6379> SADD setA 1 2 3 
    (integer) 3
    127.0.0.1:6379> SADD setB 2 3 4 
    (integer) 3
    127.0.0.1:6379> SDIFF setA setB
    1) "1"
    127.0.0.1:6379> SDIFF setB setA
    1) "4"
    127.0.0.1:6379> SINTER setA setB
    1) "2"
    2) "3"
    127.0.0.1:6379> SUNION setA setB
    1) "1"
    2) "2"
    3) "3"
    4) "4"
      
获取集合中元素的个数

    SCARD key
    127.0.0.1:6379> SMEMBERS letters
    1) "b"
    2) "a"
    127.0.0.1:6379> SCARD letters
    (integer) 2
    
进行集合运算并将结果存储

    SDIFFSTORE destination key [key ...]
    SINTERSTORE destination key [key ...]
    SUNIONSTORE destination key [key ...]
    
随机获得集合中的元素

    SRANDMEMBER key [count]
    127.0.0.1:6379> SRANDMEMBER letters
    "b"
    127.0.0.1:6379> SRANDMEMBER letters
    "b"
    127.0.0.1:6379> SRANDMEMBER letters
    "a"
    127.0.0.1:6379> SADD letters c d 
    (integer) 2
    127.0.0.1:6379> SRANDMEMBER letters 2
    1) "c"
    2) "a"
    127.0.0.1:6379> SRANDMEMBER letters 2
    1) "b"
    2) "a"
    127.0.0.1:6379> SRANDMEMBER letters 100
    1) "b"
    2) "d"
    3) "c"
    4) "a"
    127.0.0.1:6379> SRANDMEMBER letters -2
    1) "b"
    2) "b"
    127.0.0.1:6379> SRANDMEMBER letters -10
     1) "c"
     2) "b"
     3) "c"
     4) "c"
     5) "c"
     6) "d"
     7) "b"
     8) "a"
     9) "a"
    10) "d"
    127.0.0.1:6379> SRANDMEMBER letters -4
    1) "c"
    2) "a"
    3) "a"
    4) "a"
         
从集合中弹出一个元素

    SPOP key
    127.0.0.1:6379> SPOP letters 
    "c"
    127.0.0.1:6379> SMEMBERS letters
    1) "b"
    2) "d"
    3) "a"
    
## 有序集合类型（sorted set）

增加元素

    ZADD key score member [score member ...]
    127.0.0.1:6379> ZADD scoreboard 89 Tom 67 Peter 100 David
    (integer) 3
    127.0.0.1:6379> ZADD scoreboard 76 Peter
    (integer) 0
     
获取元素的分数

    ZSCORE key member
    127.0.0.1:6379> ZSCORE scoreboard Peter
    "76" 
    
获得排名在某个范围的元素列表

    ZRANDGE key start stop [WITHSCORES]  # 从小到大
    ZREVRANGE key start stop [WITHSCORES] #从大到小
    127.0.0.1:6379> ZRANGE scoreboard 0 2
    1) "Peter"
    2) "Tom"
    3) "David"
    127.0.0.1:6379> ZRANGE scoreboard 1 -1 
    1) "Tom"
    2) "David"
    127.0.0.1:6379> ZRANGE scoreboard 0 -1 withscores 
    1) "Peter"
    2) "76"
    3) "Tom"
    4) "89"
    5) "David"
    6) "100"
    
获得指定分数范围的元素

    ZRANGEBYSCORE key min max [withscores] [limit offset count]
    127.0.0.1:6379> ZRANGEBYSCORE scoreboard 80 100  # 加(表示不包含
    1) "Tom"
    2) "David" 
    127.0.0.1:6379> ZRANGEBYSCORE scoreboard 80 (100
    1) "Tom" 

增加某个元素的分数

    XINCRBY key increment member
    
获得集合中元素的数量

    ZCARD key 
    
获得指定分数范围内的元素个数

    ZCOUNT key min max 
    
删除一个或多个元素

    ZREM key member [member ...]
    
按照排名范围删除元素

    ZREMRANGEBYRANK key start stop
    
按照分数范围删除元素

    ZREMRANGEBYSCORE key min max
    
获得元素排名

    ZRANK key member
    ZRERANK key member
    

