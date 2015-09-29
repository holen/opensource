# Install elasticsearch 
install elasticsearch

    curl -L -O http://download.elasticsearch.org/PATH/TO/VERSION.zip <1>
    unzip elasticsearch-$VERSION.zip
    cd  elasticsearch-$VERSION 

install marvel plugin

    ./bin/plugin -i elasticsearch/marvel/latest

no monitor

    echo 'marvel.agent.enabled: false' >> ./config/elasticsearch.yml

run

    ./bin/elasticsearch
    curl 'http://localhost:9200/?pretty'
    curl -XPOST 'http://localhost:9200/_shutdown'
    http://localhost:9200/_plugin/marvel/
    http://localhost:9200/_plugin/marvel/sense/

# API 

    curl -X<VERB> '<PROTOCOL>://<HOST>/<PATH>?<QUERY_STRING>' -d '<BODY>'
    VERB HTTP方法：GET, POST, PUT, HEAD, DELETE
    PROTOCOL http或者https协议（只有在Elasticsearch前面有https代理的时候可用）
    HOST Elasticsearch集群中的任何一个节点的主机名，如果是在本地的节点，那么就叫localhost
    PORT Elasticsearch HTTP服务所在的端口，默认为9200
    QUERY_STRING 一些可选的查询请求参数，例如?pretty参数将使请求返回更加美观易读的JSON数据
    BODY 一个JSON格式的请求主体（如果请求需要的话）

example:

    curl -XGET 'localhost:9200/_count?pretty' -d '{ "query":{"match_all":{}}}'
    curl -XGET 'localhost:9200/_search' -d '{"query":{"match_phrase":{"about":"rock climbing"}}}'
    curl -i -XGET 'localhost:9200/'

Sense
    
    GET /_count { "query":{"match_all":{}}}

# Document

    Relational DB -> Databases -> Tables -> Rows -> Columns
    Elasticsearch -> Indices   -> Types  -> Documents -> Fields
    Elasticsearch集群可以包含多个索引(indices)（数据库），每一个索引可以包含多个类型(types)（表），每一个类型包含多个文档(documents)（行），然后每个文档包含多个字段(Fields)（列）

create document

    PUT /megacorp/employee/1
    {
        "first_name" : "John",
        "last_name" :  "Smith",
        "age" :        25,
        "about" :      "I love to go rock climbing",
        "interests": [ "sports", "music" ]
    }
    PUT /megacorp/employee/2
    {
        "first_name" :  "Jane",
        "last_name" :   "Smith",
        "age" :         32,
        "about" :       "I like to collect rock albums",
        "interests":  [ "music" ]
    }
    
    PUT /megacorp/employee/3
    {
        "first_name" :  "Douglas",
        "last_name" :   "Fir",
        "age" :         35,
        "about":        "I like to build cabinets",
        "interests":  [ "forestry" ]
    }

search one document

    GET /megacorp/employee/1

serch all document

    GET /megacorp/employee/_search

simple search

    GET /megacorp/employee/_search?q=last_name:Smith

DSL search

    GET /megacorp/employee/_search
    {
        "query" : {
            "match" : {
                "last_name" : "Smith"
            }
        }
    }

complex search (filter)

    GET /megacorp/employee/_search
    {
        "query" : {
            "filtered" : {
                "filter" : {
                    "range" : {
                        "age" : { "gt" : 30 }
                    }
                },
                "query" : {
                    "match" : {
                        "last_name" : "smith"
                    }
                }
            }
        }
    }

full text search (relevance, _score)

    GET /megacorp/employee/_search
    {
        "query" : {
            "match" : {
                "about" : "rock climbing"
            }
        }
    }

phrases search

    GET /megacorp/employee/_search
    {
        "query" : {
            "match_phrase" : {
                "about" : "rock climbing"
            }
        }
    }

highlight search

    GET /megacorp/employee/_search
    {
        "query" : {
            "match_phrase" : {
                "about" : "rock climbing"
            }
        },
        "highlight": {
            "fields" : {
                "about" : {}
            }
        }
    }

# Aggregations (GROUP BY)
search interests

    GET /megacorp/employee/_search
    {
      "aggs": {
        "all_interests": {
          "terms": { "field": "interests" }
        }
      }
    }

result

    "aggregations": {
      "all_interests": {
         "doc_count_error_upper_bound": 0,
         "sum_other_doc_count": 0,
         "buckets": [
            {
               "key": "music",
               "doc_count": 2
            },
            {
               "key": "forestry",
               "doc_count": 1
            },
            {
               "key": "sports",
               "doc_count": 1
            }
         ]
      }
   }

specipy field

    GET /megacorp/employee/_search
    {
      "query": {
        "match": {
          "last_name": "smith"
        }
      },
      "aggs": {
        "all_interests": {
          "terms": {
            "field": "interests"
          }
        }
      }
    }

聚合也允许分级汇总。例如，让我们统计每种兴趣下职员的平均年龄：

    GET /megacorp/employee/_search
    {
        "aggs" : {
            "all_interests" : {
                "terms" : { "field" : "interests" },
                "aggs" : {
                    "avg_age" : {
                        "avg" : { "field" : "age" }
                    }
                }
            }
        }
    }


