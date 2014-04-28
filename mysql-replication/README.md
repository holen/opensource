# Mysql Replication

# Install mysql on ubuntu12.04

    apt-get update
    apt-get install mysql-server mysql-client
    
# Mysql master settng
Delete the comment

    sed -i '/^#/d' /etc/mysql/my.cnf

Prepare

    mkdir -p /data/mysql
    mkdir -p /data/mysql-tmp
    mkdir -p /data/mysql-log
    chown -R mysql.root /data/mysql
    chown -R mysql.root /data/mysql-tmp
    chown -R mysql.root /data/mysql-log
    
Modify the config file --> /etc/mysql/my.cnf

    [mysqld]
    # security --> disable LOAD_DATA_LOCAL[0]
    set-variable=local-infile=0   ## mysql 5.5.34 is local-infile=0
    # master
    server-id       = 1
    binlog-format   = mixed
    log_bin         = mysql-bin
    # 将log buffer刷写到日志
    innodb_flush_log_at_trx_commit  = 1 
    # sync_binlog   = 1  将binlog与硬盘同步
    binlog-ignore-db        = mysql
    binlog-ignore-db        = performance_schema
    binlog-ignore-db        = information_schema
    replicate-ignore-db     = mysql
    replicate-ignore-db     = performance_schema
    replicate-ignore-db     = information_schema
    #############
    open_files_limit = 1000000
    skip-external-locking
    skip-name-resolve 
    ###########
    slow_query_log  = 1
    slow_query_log_file     = /data/mysql-log/slow-query.log
    long_query_time         = 2
    log-queries-not-using-indexes
    max_error_count = 65535 

Modify chroot --> /etc/apparmor.d/usr.sbin.mysqld

    /data/mysql/ r,
    /data/mysql/** rwk,
    /data/mysql-tmp/ r,
    /data/mysql-tmp/* rw,
    /data/mysql-log/ r,
    /data/mysql-log/* rw,

Create repl user

    grant replication slave, replication client on *.* to repl@'192.168.12.110' identified by 'qwer1234'; 
    flush privileges;
    show slave hosts;

Scp mysql data

    service mysql stop
    rsync -av --progress --exclude 'mysql-bin*' /data/mysql root@10.0.0.3:/data/
    rsync -av --progress --exclude 'mysql-bin*' /data/mysql root@10.0.0.3:/data/
    rsync -av --progress --exclude --delete 'mysql-bin*' /data/mysql root@10.0.0.3:/data/

## Mysql slave setting
Sync my.cnf 

    rsync -av --progress --exclude 'mysql-bin*' /data/mysql root@10.0.0.3:/data/
    rsync -av --progress --exclude 'mysql-bin*' /data/mysql root@10.0.0.3:/data/
    rsync -av --progress --exclude --delete 'mysql-bin*' /data/mysql root@10.0.0.3:/data/
    
Modify mysql config --> /etc/mysql/my.cnf

    # slave
    server-id               = 101
    binlog-format           = mixed
    log_bin                 = mysql-bin
    relay-log               = mysql-relay-bin
    log-slave-updates       = 1
    read-only               = 1
    replicate-ignore-db     = mysql
    replicate-ignore-db     = performance_schema
    replicate-ignore-db     = information_schema 
    
Set replication

    show master status;
    change master to master_host='server1',master_user='repl',master_password = 'qwer1234',master_log_file = 'mysql-bin.000001',master_log_pos=0;
    show slave status;
    start slave;
    show processlist;

Skip a error

    stop slave; set global sql_slave_skip_counter=1; start slave ;
    
## Test 
Master 

    show slave hosts;
    use test;
    create table abc(a int,b int,c int); 
    insert into abc values(1,2,3); 
    select * from abc;
    
Slave 

    use test;
    select * from abc;
                
[0]:http://dev.mysql.com/doc/refman/5.0/en/load-data.html 
