名称 	说明 	类型 	默认值 	有效值 	重要性
bootstrap.servers 	用于建立与kafka集群连接的host/port组。数据将会在所有servers上均衡加载，不管哪些server是指定用于bootstrapping。这个列表仅仅影响初始化的hosts（用于发现全部的servers）。这个列表格式：host1:port1,host2:port2,…因为这些server仅仅是用于初始化的连接，以发现集群所有成员关系（可能会动态的变化），这个列表不需要包含所有的servers（你可能想要不止一个server，尽管这样，可能某个server宕机了）。如果没有server在这个列表出现，则发送数据会一直失败，直到列表可用。 	list 			高
acks 	producer需要server接收到数据之后发出的确认接收的信号，此项配置就是指procuder需要多少个这样的确认信号。此配置实际上代表了数据备份的可用性。以下设置为常用选项：（1）acks=0： 设置为0表示producer不需要等待任何确认收到的信息。副本将立即加到socket buffer并认为已经发送。没有任何保障可以保证此种情况下server已经成功接收数据，同时重试配置不会发生作用（因为客户端不知道是否失败）回馈的offset会总是设置为-1；（2）acks=1： 这意味着至少要等待leader已经成功将数据写入本地log，但是并没有等待所有follower是否成功写入。这种情况下，如果follower没有成功备份数据，而此时leader又挂掉，则消息会丢失。（3）acks=all： 这意味着leader需要等待所有备份都成功写入日志，这种策略会保证只要有一个备份存活就不会丢失数据。这是最强的保证。， 	string 	-1 	[all -1 0 1] 	高
key.serializer 	key的序列化方式，若是没有设置，同serializer.class 	实现Serializer接口的class 			高
value.serializer 	value序列化类方式 	实现Serializer接口的class 			高
buffer.memory 	producer可以用来缓存数据的内存大小。如果数据产生速度大于向broker发送的速度，producer会阻塞或者抛出异常，以“block.on.buffer.full”来表明。这项设置将和producer能够使用的总内存相关，但并不是一个硬性的限制，因为不是producer使用的所有内存都是用于缓存。一些额外的内存会用于压缩（如果引入压缩机制），同样还有一些用于维护请求。 	long 	33554432 		高
compression.type 	producer用于压缩数据的压缩类型。默认是无压缩。正确的选项值是none、gzip、snappy。压缩最好用于批量处理，批量处理消息越多，压缩性能越好 	string 	none 		高
retries 	设置大于0的值将使客户端重新发送任何数据，一旦这些数据发送失败。注意，这些重试与客户端接收到发送错误时的重试没有什么不同。允许重试将潜在的改变数据的顺序，如果这两个消息记录都是发送到同一个partition，则第一个消息失败第二个发送成功，则第二条消息会比第一条消息出现要早。 	int 	0 		高
batch.size 	producer将试图批处理消息记录，以减少请求次数。这将改善client与server之间的性能。这项配置控制默认的批量处理消息字节数。不会试图处理大于这个字节数的消息字节数。发送到brokers的请求将包含多个批量处理，其中会包含对每个partition的一个请求。较小的批量处理数值比较少用，并且可能降低吞吐量（0则会仅用批量处理）。较大的批量处理数值将会浪费更多内存空间，这样就需要分配特定批量处理数值的内存大小。 	int 	16384 		高
client.id 	当向server发出请求时，这个字符串会发送给server。目的是能够追踪请求源头，以此来允许ip/port许可列表之外的一些应用可以发送信息。这项应用可以设置任意字符串，因为没有任何功能性的目的，除了记录和跟踪 	string 	“” 		中
connections.max.idle.ms 	关闭连接空闲时间 	long 	540000 		中
linger.ms 	producer组将会汇总任何在请求与发送之间到达的消息记录一个单独批量的请求。通常来说，这只有在记录产生速度大于发送速度的时候才能发生。然而，在某些条件下，客户端将希望降低请求的数量，甚至降低到中等负载一下。这项设置将通过增加小的延迟来完成–即，不是立即发送一条记录，producer将会等待给定的延迟时间以允许其他消息记录发送，这些消息记录可以批量处理。这可以认为是TCP种Nagle的算法类似。这项设置设定了批量处理的更高的延迟边界：一旦我们获得某个partition的batch.size，他将会立即发送而不顾这项设置，然而如果我们获得消息字节数比这项设置要小的多，我们需要“linger”特定的时间以获取更多的消息。 这个设置默认为0，即没有延迟。设定linger.ms=5，例如，将会减少请求数目，但是同时会增加5ms的延迟。 	long 	0 		中
max.block.ms 	控制block的时长,当buffer空间不够或者metadata丢失时产生block 	long 	60000 		中
max.request.size 	请求的最大字节数。这也是对最大记录尺寸的有效覆盖。注意：server具有自己对消息记录尺寸的覆盖，这些尺寸和这个设置不同。此项设置将会限制producer每次批量发送请求的数目，以防发出巨量的请求。 	int 	1048576 		中
partitioner.class 	分区类 	实现Partitioner 的class 	class org.apache.kafka.clients.producer.internals.DefaultPartitioner 		中
receive.buffer.bytes 	socket的接收缓存空间大小,当阅读数据时使用 	int 	32768 		中
request.timeout.ms 	客户端将等待请求的响应的最大时间,如果在这个时间内没有收到响应，客户端将重发请求;超过重试次数将抛异常 	int 	3000 		中
send.buffer.bytes 	发送数据时的缓存空间大小 	int 	131072 		中
timeout.ms 	此配置选项控制server等待来自followers的确认的最大时间。如果确认的请求数目在此时间内没有实现，则会返回一个错误。这个超时限制是以server端度量的，没有包含请求的网络延迟 	int 	30000 		中
max.in.flight.requests.per.connection 	kafka可以在一个connection中发送多个请求，叫作一个flight,这样可以减少开销，但是如果产生错误，可能会造成数据的发送顺序改变,默认是5 (修改） 	int 	5 		低
metadata.fetch.timeout.ms 	是指我们所获取的一些元素据的第一个时间数据。元素据包含：topic，host，partitions。此项配置是指当等待元素据fetch成功完成所需要的时间，否则会跑出异常给客户端 	long 	60000 		低
metadata.max.age.ms 	以微秒为单位的时间，是在我们强制更新metadata的时间间隔。即使我们没有看到任何partition leadership改变。 	long 	300000 		低
metric.reporters 	类的列表，用于衡量指标。实现MetricReporter接口，将允许增加一些类，这些类在新的衡量指标产生时就会改变。JmxReporter总会包含用于注册JMX统计 	list 	none 		低
metrics.num.samples 	用于维护metrics的样本数 	int 	2 		低
metrics.sample.window.ms 	metrics系统维护可配置的样本数量，在一个可修正的window size。这项配置配置了窗口大小，例如。我们可能在30s的期间维护两个样本。当一个窗口推出后，我们会擦除并重写最老的窗口 	long 	30000 		低
reconnect.backoff.ms 	连接失败时，当我们重新连接时的等待时间。这避免了客户端反复重连 	long 	10 		低
retry.backoff.ms 	在试图重试失败的produce请求之前的等待时间。避免陷入发送-失败的死循环中 	long 	100 		低
