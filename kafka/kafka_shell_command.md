查看所有topic列表

bin/kafka-topics.sh --zookeeper node01:2181 --list

查看指定topic信息

bin/kafka-topics.sh --zookeeper node01:2181 --describe --topic t_cdr

控制台向topic生产数据

bin/kafka-console-producer.sh --broker-list node86:9092 --topic t_cdr

控制台消费topic的数据

bin/kafka-console-consumer.sh  --zookeeper node01:2181  --topic t_cdr --from-beginning

查看topic某分区偏移量最大（小）值

bin/kafka-run-class.sh kafka.tools.GetOffsetShell --topic hive-mdatabase-hostsltable  --time -1 --broker-list node86:9092 --partitions 0
注： time为-1时表示最大值，time为-2时表示最小值

创建主题

bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic test_topic

添加分区

bin/kafka-topics.sh --alter --zookeeper localhost:2181 --topic test_topic --partitions 3

基本操作
列出所有topic

kafka-topics.sh --zookeeper localhost:2181 --list 

创建topic

kafka-topics.sh --zookeeper localhost:2181 \
                            --create \
                            --topic earth \
                            --partitions 1 \
                            --replication-factor 1

生产数据

向earth发送一条消息

echo "The first record" | kafka-console-producer.sh \
                    --broker-list localhost:9092 \
                    --topic earth 

向earth发送一条包含key的消息

echo '00000,{"name":"Steve", "title":"Captain America"}' | kafka-console-producer.sh \
              --broker-list localhost:9092 \
              --topic earth \
              --property parse.key=true \
              --property key.separator=,

消费数据

kafka-console-consumer.sh --zookeeper localhost:2181 \
                                      --topic earth \
                                      --from-beginning

将消息的key也输出

kafka-console-consumer.sh --zookeeper localhost:2181 \
                                      --topic earth \
                                      --from-beginning
                                      --property print.key=true \
                                      --property key.separator=,

Topic的offset统计

kafka-run-class.sh kafka.tools.GetOffsetShell \
                                 --broker-list localhost:9092 \
                                 --topic earth \
                                 --time -1

最后的参数-1表示显示获取当前offset最大值，-2表示offset的最小值

如果遇到数据倾斜的情况，可以通过kafka-simple-consumer-shell.sh查看具体某个partition数据内容，例如

kafka-simple-consumer-shell.sh --broker-list localhost:9092 \
                                       --topic earth \
                                       --partition 1 \
                                       --print-offsets \
                                       --offset 18 \
                                       --clientId test \
                                       --property print.key=true

高级Consumers和Groups

创建一个consumer.properties配置文件，指定group.id

echo "group.id=Avengers" > consumer.properties

然后再发送一条数据

echo "The second record" | kafka-console-producer.sh \
                    --broker-list localhost:9092 \
                    --topic earth 

通过consumer验证一下当前topic的数据，

kafka-console-consumer.sh --zookeeper localhost:2181 \
                                      --topic earth \
                                      --from-beginning \
                                      --consumer.config consumer.properties

得到的结果是

The first record
The second record

这是看一下zookeeper中存储的内容

[zk: localhost:2181(CONNECTED) 0] get /consumers/Avengers/offsets/earth/0
2
cZxid = 0x8200012d1d
ctime = Fri May 05 17:10:02 CST 2017
mZxid = 0x8200012d1d
mtime = Fri May 05 17:10:02 CST 2017
pZxid = 0x8200012d1d
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 1
numChildren = 0

第一行的2表示的就是我们配置的这个group消费的最后一个offset，如果再次运行

kafka-console-consumer.sh --zookeeper localhost:2181 \
                                      --topic earth \
                                      --consumer.config consumer.properties

没有任何结果输出

这时需要通过UpdateOffsetsInZK重置offset，在刚才的配置中加入

echo "zookeeper.connect=localhost:2181" >> consumer.properties

然后运行

kafka-run-class.sh kafka.tools.UpdateOffsetsInZK earliest consumer.properties earth

显示如下结果

updating partition 0 with new offset: 0
updated the offset for 1 partitions

这样运行刚才的命令

kafka-console-consumer.sh --zookeeper localhost:2181 \
                                      --topic earth \
                                      --consumer.config consumer.properties

会重新从第一个offset开始读，即显示

The first record
The second record

但是如果运行下面的命令，即加上--from-beginning

kafka-console-consumer.sh --zookeeper localhost:2181 \
                                      --topic earth \
                                      --from-beginning \
                                      --consumer.config consumer.properties

就会提示

Found previous offset information for this group Avengers. Please use --delete-consumer-offsets to delete previous offsets metadata

必须要加上--delete-consumer-offsets才可以，像这样

kafka-console-consumer.sh --zookeeper localhost:2181 \
                                      --topic earth \
                                     --delete-consumer-offsets \
                                      --from-beginning \
                                      --consumer.config consumer.properties


验证消息生产成功
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092,localhost:9093,localhost:9094 --topic test --time -1
注： --time 的值 -1代表最大值， -2代表最小值

创建一个console consumer group

bin/kafka-console-consumer.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --topic test --from-beginning --new-consumer

获取该consumer group的group id(后面需要根据该id查询它的位移信息)

bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092,localhost:9093,localhost:9094 --list --new-consumer

查看当前group的消费情况

./kafka-consumer-groups.sh -bootstrap-server localhost:9092 --describe --group test

# 获取指定consumer group的位移信息 
bin/kafka-simple-consumer-shell.sh --topic __consumer_offsets --partition 11 --broker-list localhost:9092,localhost:9093,localhost:9094 --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter"

[test,test,0]::[OffsetMetadata[176955,NO_METADATA],CommitTime 1522069325297,ExpirationTime 1522155725297]
[test,test,0]::[OffsetMetadata[176955,NO_METADATA],CommitTime 1522069326298,ExpirationTime 1522155726298]
[test,test,0]::[OffsetMetadata[176955,NO_METADATA],CommitTime 1522069327299,ExpirationTime 1522155727299]
上图可见，该consumer group果然保存在分区11上，且位移信息都是对的(这里的位移信息是已消费的位移，严格来说不是第3步中的位移。由于我的consumer已经消费完了所有的消息，所以这里的位移与第3步中的位移相同)。另外，可以看到__consumer_offsets topic的每一日志项的格式都是：[Group, Topic, Partition]::[OffsetMetadata[Offset, Metadata], CommitTime, ExpirationTime]


# ref https://www.jianshu.com/p/5aa8776868bb
