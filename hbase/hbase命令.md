# HBase 命令

通用命令

    status: 提供HBase的状态，例如，服务器的数量。
    version: 提供正在使用HBase版本。
    table_help: 表引用命令提供帮助。
    whoami: 提供有关用户的信息

数据定义语言

这些是关于HBase在表中操作的命令。

    create: 创建一个表。
    list: 列出HBase的所有表。
    disable: 禁用表。
    is_disabled: 验证表是否被禁用。
    enable: 启用一个表。
    is_enabled: 验证表是否已启用。
    describe: 提供了一个表的描述。
    alter: 改变一个表。
    exists: 验证表是否存在。
    drop: 从HBase中删除表。
    drop_all: 丢弃在命令中给出匹配“regex”的表。
    Java Admin API: 在此之前所有的上述命令，Java提供了一个通过API编程来管理实现DDL功能。在这个org.apache.hadoop.hbase.client包中有HBaseAdmin和HTableDescriptor 这两个重要的类提供DDL功能。

数据操纵语言

    put: 把指定列在指定的行中单元格的值在一个特定的表。
    get: 取行或单元格的内容。
    delete: 删除表中的单元格值。
    deleteall: 删除给定行的所有单元格。
    scan: 扫描并返回表数据。
    count: 计数并返回表中的行的数目。
    truncate: 禁用，删除和重新创建一个指定的表。
    Java client API: 在此之前所有上述命令，Java提供了一个客户端API来实现DML功能，CRUD（创建检索更新删除）操作更多的是通过编程，在org.apache.hadoop.hbase.client包下。 在此包HTable 的 Put和Get是重要的类

Hbase 权限控制

grant命令授予特定的权限，如读，写，执行和管理表给定一个特定的用户。 grant命令的语法如下：

	hbase> grant <user> <permissions> [<table> [<column family> [<column; qualifier>]]

我们可以从RWXCA组，其中给予零个或多个特权给用户

    R - 代表读取权限
    W - 代表写权限
    X - 代表执行权限
    C - 代表创建权限
    A - 代表管理权限

下面给出是为用户“Tutorialspoint'授予所有权限的例子。

	hbase(main):018:0> grant 'Tutorialspoint', 'RWXCA'

revoke命令用于撤销用户访问表的权限。它的语法如下：

	hbase> revoke <user>

下面的代码撤消名为“Tutorialspoint”用户的所有权限。

	hbase(main):006:0> revoke 'Tutorialspoint'

user_permission 此命令用于列出特定表的所有权限。 user_permission的语法如下：

	hbase>user_permission ‘tablename’

下面的代码列出了“emp”表的所有用户权限。

	hbase(main):013:0> user_permission 'emp'
