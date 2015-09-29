# one instance
check cluster health

    GET /_cluster/health

shareds (primary shared , replica share)  
索引中的每个文档属于一个单独的主分片，所以主分片的数量决定了索引最多能存储多少数据  
复制分片只是主分片的一个副本，它可以防止硬件故障导致的数据丢失，同时可以提供读请求，比如搜索或者从别的shard取回文档  
当索引创建完成的时候，主分片的数量就固定了，但是复制分片的数量可以随时调整  

    PUT /blogs
    {
       "settings" : {
          "number_of_shards" : 3,
          "number_of_replicas" : 1
       }
    }

    GET /_cluster/health

