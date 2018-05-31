hdfs 副本块不足

    su hdfs                 # 切换到hdfs用户
    hadoop fsck /           # 检查hdfs块信息
    hadoop fs -setrep 1 /   # 配置dfs.replication值为1

