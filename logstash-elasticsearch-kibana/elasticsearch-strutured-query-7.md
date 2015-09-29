# Request body search 
empty search

    GET /_search
    {}

    GET /index_2014*/type1,type2/_search
    {}

    POST /_search
    {
      "from": 30,
      "size": 10
    }

# Query DSL
查询子句  

一个查询子句一般使用这种结构：

    {
        QUERY_NAME: {
            ARGUMENT: VALUE,
            ARGUMENT: VALUE,...
        }
    }

    {
        "match": {
            "tweet": "elasticsearch"
        }
    }

或指向一个指定的字段：

    {
        QUERY_NAME: {
            FIELD_NAME: {
                ARGUMENT: VALUE,
                ARGUMENT: VALUE,...
            }
        }
    }

    GET /_search
    {
        "query": {
            "match": {
                "tweet": "elasticsearch"
            }
        }
    }

# query DSL &  filter DSL
使用查询语句做全文本搜索或其他需要进行相关性评分的时候，剩下的全部用过滤语句

# 最重要的查询过滤语句
term 主要用于精确匹配哪些值，比如数字，日期，布尔值或 not_analyzed的字符串(未经分析的文本数据类型)：

    { "term": { "age":    26           }}
    { "term": { "date":   "2014-09-01" }}
    { "term": { "public": true         }}
    { "term": { "tag":    "full_text"  }}

terms 跟 term 有点类似，但 terms 允许指定多个匹配条件。 如果某个字段指定了多个值，那么文档需要一起去做匹配：

    {
        "terms": {
            "tag": [ "search", "full_text", "nosql" ]
            }
    }

range过滤允许我们按照指定范围查找一批数据：

    {
        "range": {
            "age": {
                "gte":  20,
                "lt":   30
            }
        }
    }
    
exists 和 missing 过滤可以用于查找文档中是否包含指定字段或没有某个字段，类似于SQL语句中的IS_NULL条件

    {
        "exists":   {
            "field":    "title"
        }
    }

bool 过滤可以用来合并多个过滤条件查询结果的布尔逻辑，它包含一下操作符：  
must :: 多个查询条件的完全匹配,相当于 and。  
must_not :: 多个查询条件的相反匹配，相当于 not。  
should :: 至少有一个查询条件匹配, 相当于 or。  
这些参数可以分别继承一个过滤条件或者一个过滤条件的数组：  

    {
        "bool": {
            "must":     { "term": { "folder": "inbox" }},
            "must_not": { "term": { "tag":    "spam"  }},
            "should": [
                        { "term": { "starred": true   }},
                        { "term": { "unread":  true   }}
            ]
        }
    }

match_all 可以查询到所有文档，是没有查询条件下的默认语句。

    {
        "match_all": {}
    }
    
match 查询一个全文本字段，它会在真正查询之前用分析器先分析match一下查询字符：

    {
        "match": {
            "tweet": "About Search"
        }
    }

match下指定了一个确切值，在遇到数字，日期，布尔值或者not_analyzed 的字符串时，它将为你搜索你给定的值：
    
    { "match": { "age":    26           }}
    { "match": { "date":   "2014-09-01" }}
    { "match": { "public": true         }}
    { "match": { "tag":    "full_text"  }}
    
multi_match查询允许你做match查询的基础上同时搜索多个字段：

    {
        "multi_match": {
            "query":    "full text search",
            "fields":   [ "title", "body" ]
        }
    }

bool 查询与 bool 过滤相似，用于合并多个查询子句。不同的是，bool 过滤可以直接给出是否匹配成功， 而bool 查询要计算每一个查询子句的 _score （相关性分值）。  
must:: 查询指定文档一定要被包含。  
must_not:: 查询指定文档一定不要被包含。  
should:: 查询指定文档，有则可以为文档相关性加分。  
以下查询将会找到 title 字段中包含 "how to make millions"，并且 "tag" 字段没有被标为 spam。 如果有标识为 "starred" 或者发布日期为2014年之前，那么这些匹配的文档将比同类网站等级高：

    {
        "bool": {
            "must":     { "match": { "title": "how to make millions" }},
            "must_not": { "match": { "tag":   "spam" }},
            "should": [
                { "match": { "tag": "starred" }},
                { "range": { "date": { "gte": "2014-01-01" }}}
            ]
        }
    }

# 过滤查询
query , filter 

    GET /_search
    {
        "query": {
            "filtered": {
                "query":  { "match": { "email": "business opportunity" }},
                "filter": { "term": { "folder": "inbox" }}
            }
        }
    }

# 验证查询
validata api

    GET /gb/tweet/_validate/query
    {
       "query": {
          "tweet" : {
             "match" : "really powerful"
          }
       }
    }
    
    GET /gb/tweet/_validate/query?explain <1>
    {
       "query": {
          "tweet" : {
             "match" : "really powerful"
          }
       }
    }
    
    GET /_validate/query?explain
    {
       "query": {
          "match" : {
             "tweet" : "really powerful"
          }
       }
    }
