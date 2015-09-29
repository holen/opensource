# Search
概念

    映射(Mapping)   数据在每个字段中的解释说明,字段类型确认
    分析(Analysis)  全文是如何处理的可以被搜索的,Full Text的分词
    领域特定语言查询(Query DSL) Elasticsearch使用的灵活的、强大的查询语言

empty search

    GET /_search
    GET /_search?timeout=10ms

多索引和多类型

    /_search
    在所有索引的所有类型中搜索
    
    /gb/_search
    在索引gb的所有类型中搜索
    
    /gb,us/_search
    在索引gb和us的所有类型中搜索
    
    /g*,u*/_search
    在以g或u开头的索引的所有类型中搜索
    
    /gb/user/_search
    在索引gb的类型user中搜索
    
    /gb,us/user,tweet/_search
    在索引gb和us的类型为user和tweet中搜索
    
    /_all/user,tweet/_search
    在所有索引的user和tweet中搜索 search types user and tweet in all indices

分页

    size: 果数，默认10
    from: 跳过开始的结果数，默认0

    如果你想每页显示5个结果，页码从1到3，那请求如下：
    GET /_search?size=5
    GET /_search?size=5&from=5
    GET /_search?size=5&from=10

query string and request body

    GET /_all/tweet/_search?q=tweet:elasticsearch
    GET /_search?q=%2Bname%3Ajohn+%2Btweet%3Amary  # +name:john +tweet:mary (percent encoding)
    GET /_search?q=mary
   
   
