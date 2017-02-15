Property 	Default 	Description
group.id 		用来唯一标识consumer进程所在组的字符串，如果设置同样的group id，表示这些processes都是属于同一个consumer group
zookeeper.connect 		指定zookeeper的连接的字符串，格式是hostname：port，此处host和port都是zookeeper server的host和port，为避免某个zookeeper 机器宕机之后失联，你可以指定多个hostname：port，使用逗号作为分隔：hostname1：port1，hostname2：port2，hostname3：port3可以在zookeeper连接字符串中加入zookeeper的chroot路径，此路径用于存放他自己的数据，方式：hostname1：port1，hostname2：port2，hostname3：port3/chroot/path
consumer.id 	null 	不需要设置，一般自动产生
socket.timeout.ms 	30*1000 	网络请求的超时限制。真实的超时限制是 max.fetch.wait+socket.timeout.ms
socket.receive.buffer.bytes 	64*1024 	socket用于接收网络请求的缓存大小
fetch.message.max.bytes 	1024*1024 	每次fetch请求中，针对每次fetch消息的最大字节数。这些字节将会督导用于每个partition的内存中，因此，此设置将会控制consumer所使用的memory大小。这个fetch请求尺寸必须至少和server允许的最大消息尺寸相等，否则，producer可能发送的消息尺寸大于consumer所能消耗的尺寸。
num.consumer.fetchers 	1 	用于fetch数据的fetcher线程数
auto.commit.enable 	true 	如果为真，consumer所fetch的消息的offset将会自动的同步到zookeeper。这项提交的offset将在进程挂掉时，由新的consumer使用
auto.commit.interval.ms 	60*1000 	consumer向zookeeper提交offset的频率
queued.max.message.chunks 	2 	用于缓存消息的最大数目，以供consumption。每个chunk必须和fetch.message.max.bytes相同
rebalance.max.retries 	4 	当新的consumer加入到consumer group时，consumers集合试图重新平衡分配到每个consumer的partitions数目。如果consumers集合改变了，当分配正在执行时，这个重新平衡会失败并重入
fetch.min.bytes 	1 	每次fetch请求时，server应该返回的最小字节数。如果没有足够的数据返回，请求会等待，直到足够的数据才会返回。
fetch.wait.max.ms 	100 	如果没有足够的数据能够满足fetch.min.bytes，则此项配置是指在应答fetch请求之前，server会阻塞的最大时间。
rebalance.backoff.ms 	2000 	在重试reblance之前backoff时间
refresh.leader.backoff.ms 	200 	在试图确定某个partition的leader是否失去他的leader地位之前，需要等待的backoff时间
auto.offset.reset 	largest 	zookeeper中没有初始化的offset时，如果offset是以下值的回应：smallest：自动复位offset为smallest的offsetlargest：自动复位offset为largest的offsetanything else：向consumer抛出异常
consumer.timeout.ms 	-1 	如果没有消息可用，即使等待特定的时间之后也没有，则抛出超时异常
exclude.internal.topics 	true 	是否将内部topics的消息暴露给consumer
paritition.assignment.strategy 	range 	选择向consumer 流分配partitions的策略，可选值：range，roundrobin
client.id 	group id value 	是用户特定的字符串，用来在每次请求中帮助跟踪调用。它应该可以逻辑上确认产生这个请求的应用
zookeeper.session.timeout.ms 	6000 	zookeeper 会话的超时限制。如果consumer在这段时间内没有向zookeeper发送心跳信息，则它会被认为挂掉了，并且reblance将会产生
zookeeper.connection.timeout.ms 	6000 	客户端在建立通zookeeper连接中的最大等待时间
zookeeper.sync.time.ms 	2000 	ZK follower可以落后ZK leader的最大时间
offsets.storage 	zookeeper 	用于存放offsets的地点： zookeeper或者kafka
offset.channel.backoff.ms 	1000 	重新连接offsets channel或者是重试失败的offset的fetch/commit请求的backoff时间
offsets.channel.socket.timeout.ms 	10000 	当读取offset的fetch/commit请求回应的socket 超时限制。此超时限制是被consumerMetadata请求用来请求offset管理
offsets.commit.max.retries 	5 	重试offset commit的次数。这个重试只应用于offset commits在shut-down之间。
dual.commit.enabled 	true 	如果使用“kafka”作为offsets.storage，你可以二次提交offset到zookeeper(还有一次是提交到kafka）。在zookeeper-based的offset storage到kafka-based的offset storage迁移时，这是必须的。对任意给定的consumer group来说，比较安全的建议是当完成迁移之后就关闭这个选项
partition.assignment.strategy 	range 	在“range”和“roundrobin”策略之间选择一种作为分配partitions给consumer 数据流的策略； 循环的partition分配器分配所有可用的partitions以及所有可用consumer 线程。它会将partition循环的分配到consumer线程上。如果所有consumer实例的订阅都是确定的，则partitions的划分是确定的分布。循环分配策略只有在以下条件满足时才可以：（1）每个topic在每个consumer实力上都有同样数量的数据流。（2）订阅的topic的集合对于consumer group中每个consumer实例来说都是确定的。
