# Redis transaction

transaction

    127.0.0.1:6379> MULTI 
    OK
    127.0.0.1:6379> SADD "user:1:following" 2
    QUEUED
    127.0.0.1:6379> SADD "user:2:followers" 1 
    QUEUED
    127.0.0.1:6379> EXEC 
    1) (integer) 1
    2) (integer) 1

watch # 监控一个或多个键，一旦其中有一个键被修改，之后的事物就不会执行

    127.0.0.1:6379> SET key 1 
    OK
    127.0.0.1:6379> WATCH key
    OK
    127.0.0.1:6379> set key 2 
    OK
    127.0.0.1:6379> MULTI 
    OK
    127.0.0.1:6379> set key 3 
    QUEUED
    127.0.0.1:6379> exec
    (nil)
    127.0.0.1:6379> get key
    "2"

EXPIRE # 设置一个键的生存时间，到时间后Redis会自动删除它

    127.0.0.1:6379> set session:29e3d uid1314
    OK
    127.0.0.1:6379> EXPIRE session:29e3d 900
    (integer) 1
    
TTL # 返回键的剩余时间（秒）

    127.0.0.1:6379> TTL session:29e3d
    (integer) 512 
    
PERSIST # 取消键的生存时间 （set和getset命令也会消除键的生存时间）

    127.0.0.1:6379> set foo bar
    OK
    127.0.0.1:6379> EXPIRE foo 20
    (integer) 1
    127.0.0.1:6379> PERSIST foo
    (integer) 1
    127.0.0.1:6379> TTL foo
    (integer) -1
 
设置内存
    
    maxmemory <bytes> 
    maxmemory-policy volatile-lru 
    
排序 SORT

    127.0.0.1:6379> LPUSH mylist 4 2 6 1 3 7 # 集合
    (integer) 6
    127.0.0.1:6379> SORT mylist
    1) "1"
    2) "2"
    3) "3"
    4) "4"
    5) "6"
    6) "7"
    127.0.0.1:6379> ZADD myzset 50 2 40 3 20 1 60 5 # 有序集合会忽略元素的分素
    (integer) 4
    127.0.0.1:6379> SORT myzset
    1) "1"
    2) "2"
    3) "3"
    4) "5"
    127.0.0.1:6379> LPUSH mylistalpha a c e d B C A 
    (integer) 7
    127.0.0.1:6379> SORT mylistalpha
    (error) ERR One or more scores can't be converted into double
    127.0.0.1:6379> SORT mylistalpha ALPHA
    1) "a"
    2) "A"
    3) "B"
    4) "c"
    5) "C"
    6) "d"
    7) "e"
    127.0.0.1:6379> SORT tag:ruby:posts DESC LIMIT 1 2 
    
BY
 
    127.0.0.1:6379> LPUSH sortbylist 2 1 3 
    (integer) 3
    127.0.0.1:6379> SET itemscore:1 50
    OK
    127.0.0.1:6379> SET itemscore:2 100
    OK
    127.0.0.1:6379> SET itemscore:3 -10
    OK
    127.0.0.1:6379> SORT sortbylist by itemscore:* desc
    1) "2"
    2) "1"
    3) "3"
    redis> SORT sortbylist BY somekey->somefield:*    
    
BY GET

    redis> SORT tag:ruby:posts BY post:*->time DESC GET post:*->title
    按排序后直接返回ID对应的文章标题
    


