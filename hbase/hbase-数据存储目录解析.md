# hbase 数据存储目录解析

[hdfs@iZuf644h2jkgvj032edyh3Z root]$ hadoop fs -ls /hbase/data/default/test
Found 3 items
drwxr-xr-x   - hbase hbase          0 2018-05-31 16:15 /hbase/data/default/test/.tabledesc      # 表的元数据信息(具体文件)
drwxr-xr-x   - hbase hbase          0 2018-05-31 16:15 /hbase/data/default/test/.tmp            # 临时数据区
drwxr-xr-x   - hbase hbase          0 2018-05-31 16:15 /hbase/data/default/test/1593dd920697686b4408bf423b924de1    # 表数据目录


