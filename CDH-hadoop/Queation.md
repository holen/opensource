# hdfs 副本块不足

    su hdfs                 # 切换到hdfs用户
    hadoop fsck /           # 检查hdfs块信息
    hadoop fs -setrep 1 /   # 配置dfs.replication值为1

# 从Sqoop导入Mysql数据到Hbase的时候, HRegionServer 服务进程挂掉
日志：java.io.IOException: Premature EOF from inputStream

解决办法:

    修改每个datanode节点的hadoop配置文件hdfs-site.xml：
    增加dfs.datanode.max.transfer.threads属性的设置，设置为8192

    <property><name>dfs.datanode.max.transfer.threads</name> <value>8192</value></property> 

    添加Hbase RegionServer的java堆内存

    sqoop import 设置并行参数 "--num-mappers"
        -m,--num-mappers <n>                                          Use 'n' map tasks to import in parallel

# 使用Python程序通过 Thrift server导入Mysql数据时，Hbase Thrift Server 进程退出状态
错误日志：The health test result for HBASE_THRIFT_SERVER_UNEXPECTED_EXITS has become bad: This role encountered 1 unexpected exit(s) in the previous 5 minute(s).This included 1 exit(s) due to OutOfMemory errors. Critical threshold: any.

    增加Hbase Thrift Server 的heapsize 
