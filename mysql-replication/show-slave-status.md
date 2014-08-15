# SQL 的DDL,DCL,DML语言
DDL

    --Data Definition Language 数据库定义语言，如create procedure，create database/tables 之类

DML

    ----Data Manipulation Language 数据操纵语言,如insert,delete,update,select(插入、删除、修改、检索)

DCL

    ----Data Control Language 数据库控制言,如grant,deny,revoke等，只有管理员才有这样的权限

# 利用 MRG_MyISAM 存储引擎实现分表
MRG\_MyISAM

    MRG_MyISAM引擎,是一个相同的可以被当作一个来用的MyISAM表的集合."相同"意味着所有表同样的列和索引信息.你不能合并列被以不同顺序列于其中的表,没有恰好同样列的表,或有不同顺序索引的表.而且,任何或者所有的表可以用myisampack来压缩

    eg:
    mysql> create table test1 (id int not null auto_increment,name varchar(10) default null ,primary key (id)) engine=myisam auto_increment=1;            
    Query OK, 0 rows affected (0.01 sec)
    mysql> create table test2 (id int not null auto_increment,name varchar(10) default null ,primary key (id)) engine=myisam auto_increment=1; 
    Query OK, 0 rows affected (0.00 sec)
    mysql> INSERT INTO `test1` (`name`) VALUES('beijing1');   
    Query OK, 1 row affected (0.00 sec)
    mysql> INSERT INTO `test2` (`name`) VALUES('beijing2'); 
    Query OK, 1 row affected (0.00 sec)
    mysql> create table test (id int not null auto_increment,name varchar(10) default null ,index(id)) engine=mrg_myisam union=(test1,test2) insert_method=last auto_increment=1;
    Query OK, 0 rows affected (0.03 sec)

    在这里需要注意建立MRG_MYISAM需要必须指定一个UNION=(list-of-tables)子句,它说明你要把哪些表当作一个表来用.另外一个重要的参数INSERT_METHOD,此参数INSERT_METHOD = NO 表示该表不能做任何写入操作只作为查询使用,INSERT_METHOD = LAST表示插入到最后的一张表里面.

# mysql commond

    show engines
    show variables like '%wait_time%'
    set global wait_time=600
    show create table table_name
    desc table_name

# SHOW SLAVE STATUS 
Slave\_IO\_State

    SHOW PROCESSLIST输出的State字段的拷贝。SHOW PROCESSLIST用于从属I/O线程。如果线程正在试图连接到主服务器，正在等待来自主服务器的时间或正在连接到主服务器等，本语句会通知您

Master\_User

    被用于连接主服务器的当前用户。

Master\_Port

    当前的主服务器接口。

Connect\_Retry

    --master-connect-retry选项的当前值

Master\_Log\_File

    I/O线程当前正在读取的主服务器二进制日志文件的名称。

Read\_Master\_Log\_Pos

    在当前的主服务器二进制日志中，I/O线程已经读取的位置。

Relay\_Log\_File

    SQL线程当前正在读取和执行的中继日志文件的名称。

Relay\_Log\_Pos

    在当前的中继日志中，SQL线程已读取和执行的位置。

Relay\_Master\_Log\_File

    由SQL线程执行的包含多数近期事件的主服务器二进制日志文件的名称。

Slave\_IO\_Running

    I/O线程是否被启动并成功地连接到主服务器上。

Slave\_SQL\_Running

    SQL线程是否被启动。

Replicate\_Do\_DB,Replicate\_Ignore\_DB

    使用--replicate-do-db和--replicate-ignore-db选项指定的数据库清单。
    Replicate_Do_Table,Replicate_Ignore_Table,Replicate_Wild_Do_Table,Replicate_Wild_Ignore_Table
    使用--replicate-do-table,--replicate-ignore-table,--replicate-wild-do-table和--replicate-wild-ignore_table选项指定的表清单。

Last\_Errno,Last\_Error

    被多数最近被执行的查询返回的错误数量和错误消息。错误数量为0并且消息为空字符串意味着“没有错误”。如果Last_Error值不是空值，它也会在从属服务器的错误日志中作为消息显示。
    举例说明：
    Last_Errno: 1051
    Last_Error: error 'Unknown table 'z'' on query 'drop table z'
    该消息指示，表z曾经存在于在主服务器中并已被取消了，但是它没有在从属服务器中存在过，因此对于从属服务器，DROP TABLE失败。（举例说明，在设置复制时，如果您忘记了把此表拷贝到从属服务器中，则这有可能发生。）

Skip\_Counter

    最近被使用的用于SQL_SLAVE_SKIP_COUNTER的值。

Exec\_Master\_Log\_Pos

    来自主服务器的二进制日志的由SQL线程执行的上一个时间的位置（Relay_Master_Log_File）。在主服务器的二进制日志中的(Relay_Master_Log_File,Exec_Master_Log_Pos)对应于在中继日志中的(Relay_Log_File,Relay_Log_Pos)。

Relay\_Log\_Space

    所有原有的中继日志结合起来的总大小。

Until\_Condition,Until\_Log\_File,Until\_Log\_Pos

    在START SLAVE语句的UNTIL子句中指定的值。

    Until_Condition具有以下值：
    如果没有指定UNTIL子句，则没有值
    如果从属服务器正在读取，直到达到主服务器的二进制日志的给定位置为止，则值为Master
    如果从属服务器正在读取，直到达到其中继日志的给定位置为止，则值为Relay
    Until_Log_File和Until_Log_Pos用于指示日志文件名和位置值。日志文件名和位置值定义了SQL线程在哪个点中止执行。

Master\_SSL\_Allowed,Master\_SSL\_CA\_File,Master\_SSL\_CA\_Path,Master\_SSL\_Cert,Master\_SSL\_Cipher,Master\_SSL\_Key

    这些字段显示了被从属服务器使用的参数。这些参数用于连接主服务器。

Master\_SSL\_Allowed具有以下值：

    如果允许对主服务器进行SSL连接，则值为Yes
    如果不允许对主服务器进行SSL连接，则值为No
    如果允许SSL连接，但是从属服务器没有让SSL支持被启用，则值为Ignored。
    与SSL有关的字段的值对应于--master-ca,--master-capath,--master-cert,--master-cipher和--master-key选项的值。

Seconds\_Behind\_Master

    本字段是从属服务器“落后”多少的一个指示。当从属SQL线程正在运行时（处理更新），本字段为在主服务器上由此线程执行的最近的一个事件的时间标记开始，已经过的秒数。当此线程被从属服务器I/O线程赶上，并进入闲置状态，等待来自I/O线程的更多的事件时，本字段为零。总之，本字段测量从属服务器SQL线程和从属服务器I/O线程之间的时间差距，单位以秒计。
    如果主服务器和从属服务器之间的网络连接较快，则从属服务器I/O线程会非常接近主服务器，所以本字段能够十分近似地指示，从属服务器SQL线程比主服务器落后多少。如果网络较慢，则这种指示不准确；从属SQL线程经常会赶上读取速度较慢地从属服务器I/O线程，因此，Seconds_Behind_Master经常显示值为0。即使I/O线程落后于主服务器时，也是如此。换句话说，本列只对速度快的网络有用。
    即使主服务器和从属服务器不具有相同的时钟，时间差计算也会起作用（当从属服务器I/O线程启动时，计算时间差。并假定从此时以后，时间差保持不变）。如果从属SQL线程不运行，或者如果从属服务器I/O线程不运行或未与主服务器连接，则Seconds_Behind_Master为NULL（意义为“未知”）。举例说明，如果在重新连接之前，从属服务器I/O线程休眠了master-connect-retry秒，则显示NULL，因为从属服务器不知道主服务器正在做什么，也不能有把握地说落后多少。
