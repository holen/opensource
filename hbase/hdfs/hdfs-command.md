 HDFS的文件列表

加载服务器信息后，使用'ls' 可以找出文件列表中的目录，文件状态。下面给出的是ls，可以传递一个目录或文件名作为参数的语法。

	$HADOOP_HOME/bin/hadoop fs -ls <args>

将数据插入到HDFS

假设在本地系统，这是所谓的file.txt文件中的数据,应当保存在HDFS文件系统。按照下面给出插入在Hadoop的文件系统所需要的文件的步骤。
第1步

必须创建一个输入目录。

	$HADOOP_HOME/bin/hadoop fs -mkdir /user/input 

第2步

传输并使用本地系统put命令，Hadoop文件系统中存储的数据文件。

	$HADOOP_HOME/bin/hadoop fs -put /home/file.txt /user/input 

第3步

可以使用ls命令验证文件。

	$HADOOP_HOME/bin/hadoop fs -ls /user/input 

从HDFS中检索数据

假设在HDFS文件名为outfile。下面给出的是一个简单的演示用于检索从Hadoop文件系统所需的文件。
第1步

最初，使用cat命令来查看来自HDFS的数据。

	$HADOOP_HOME/bin/hadoop fs -cat /user/output/outfile 

第2步

从HDFS得到文件使用get命令在本地文件系统。

	$HADOOP_HOME/bin/hadoop fs -get /user/output/ /home/hadoop_tp/ 

