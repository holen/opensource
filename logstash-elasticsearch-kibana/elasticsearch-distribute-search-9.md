# 分布式搜索
搜索的执行过程分两个阶段，称为查询然后取回（query then fetch）

# query
查询阶段包含以下三步：

1.客户端发送一个search（搜索）请求给Node 3,Node 3创建了一个长度为from+size的空优先级队列。 
2.Node 3 转发这个搜索请求到索引中每个分片的原本或副本。每个分片在本地执行这个查询并且结果将结果到一个大小为from+size的有序本地优先队列里去。 
3.每个分片返回document的ID和它优先队列里的所有document的排序值给协调节点Node 3。Node 3把这些值合并到自己的优先队列里产生全局排序结果。

当一个搜索请求被发送到一个节点Node，这个节点就变成了协调节点。这个节点的工作是向所有相关的分片广播搜索请求并且把它们的响应整合成一个全局的有序结果集。这个结果集会被返回给客户端。

# fetch
取回阶段由以下步骤构成：

1.协调节点辨别出哪个document需要取回，并且向相关分片发出GET请求。
2.每个分片加载document并且根据需要丰富（enrich）它们，然后再将document返回协调节点。
3.一旦所有的document都被取回，协调节点会将结果返回给客户端

# 搜索选项
preference（偏爱）
    
    _primary， _primary_first， _local， _only_node:xyz， _prefer_node:xyz和_shards:2,3
    curl localhost:9200/_search?preference=xyzabc123 -d '{"query":{"match":{"title":"elasticsearch"}}}'

结果震荡（Bouncing Results）

    两个有相同字段的document可能在原始分片里是一种顺序，在副本分片里是另一种顺序
    避免这个问题方法是对于同一个用户总是使用同一个分片。方法就是使用一个随机字符串例如用户的会话ID（session ID）来设置preference参数

timeout（超时）
    
    告诉协调节点最多等待多久，就可以放弃等待而将已有结果返回

routing（路由选择）

    GET /_search?routing=user_1,user2 

search_type（搜索类型）

    GET /_search?search_type=count

count（计数）

    count（计数）搜索类型只有一个query（查询）的阶段。当不需要搜索结果只需要知道满足查询的document的数量时，可以使用这个查询类型

query_and_fetch（查询并且取回）

    query_and_fetch（查询并且取回）搜索类型将查询和取回阶段合并成一个步骤。这是一个内部优化选项，当搜索请求的目标只是一个分片时可以使用，例如指定了routing（路由选择）值时

scan（扫描）

    scan（扫描）搜索类型是和scroll（滚屏）API连在一起使用的，可以高效地取回巨大数量的结果。它是通过禁用排序来实现的

# scan-and-scroll
scroll

    一个滚屏搜索允许我们做一个初始阶段搜索并且持续批量从Elasticsearch里拉取结果直到没有结果剩下。这有点像传统数据库里的cursors（游标）

scan

    扫描模式让Elasticsearch不排序，只要分片里还有结果可以返回，就返回一批结果

example

    GET /old_index/_search?search_type=scan&scroll=1m (1)
    {
        "query": { "match_all": {}},
        "size":  1000
    }
