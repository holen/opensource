# 结构化搜索
通过结构化搜索，你的查询结果始终是 是或非；是否应该属于集合。结构化搜索不关心文档的相关性或分数，它只是简单的包含或排除文档

# 查询准确值
term: 为了使用 term 过滤器，我们需要将它包含在一个过滤查询语句中

    POST /my_store/products/_bulk
    { "index": { "_id": 1 }}
    { "price" : 10, "productID" : "XHDK-A-1293-#fJ3" }
    { "index": { "_id": 2 }}
    { "price" : 20, "productID" : "KDKE-B-9947-#kL5" }
    { "index": { "_id": 3 }}
    { "price" : 30, "productID" : "JODL-X-1937-#pV7" }
    { "index": { "_id": 4 }}
    { "price" : 30, "productID" : "QQPX-R-3956-#aD8" }

    GET /my_store/products/_search
    {
        "query" : {
            "filtered" : { 
                "query" : {
                    "match_all" : {}
                },
                "filter" : {
                    "term" : {
                        "price" : 20
                    }
                }
            }
        }
    }

用于文本的term过滤,需指定文本为not_analyzed

    DELETE /my_store <1>
    PUT /my_store <2>
    {
        "mappings" : {
            "products" : {
                "properties" : {
                    "productID" : {
                        "type" : "string",
                        "index" : "not_analyzed" <3>
                    }
                }
            }
        }
    
    }

内部过滤操作,Elasticsearch 在内部会通过一些操作来执行一次过滤：

    1.查找匹配文档。
    term 过滤器在倒排索引中查找词 XHDK-A-1293-#fJ3，然后返回包含那个词的文档列表。在这个例子中，只有文档 1 有我们想要的词。
    2.创建字节集
    然后过滤器将创建一个 字节集 —— 一个由 1 和 0 组成的数组 —— 描述哪些文档包含这个词。匹配的文档得到 1 字节，在我们的例子中，字节集将是 [1,0,0,0]
    3.缓存字节集
    最后，字节集被储存在内存中，以使我们能用它来跳过步骤 1 和 2。这大大的提升了性能，让过滤变得非常的快。

    当执行 filtered 查询时，filter 会比 query 早执行。结果字节集会被传给 query 来跳过已经被排除的文档。这种过滤器提升性能的方式，查询更少的文档意味着更快的速度,更详细的过滤条件应该被放置在其他过滤器之前.
    大部分直接处理字段的枝叶过滤器（例如 term）会被缓存，而像 bool 这类的组合过滤器则不会被缓存(脚本过滤器，Geo定位过滤器，日期范围)

组合过滤

    {
       "bool" : {
          "must" :     [],
          "should" :   [],
          "must_not" : [],
       }
    }

查询多个准确值

    {
        "terms" : {
            "price" : [20, 30]
        }
    }   

包含而不是相等

    term 和 terms 是 必须包含 操作，而不是 必须相等

范围

    "range" : {
        "price" : {
            "gt" : 20,
            "lt" : 40
        }
    }


