# ik plugin (elastic: 5.0.1 ik: 5.0.1)
Make package
    
    apt-get install maven
    git clone https://github.com/medcl/elasticsearch-analysis-ik
    cd elasticsearch-analysis-ik
    git checkout master
    mvn clean
    mvn compile
    mvn package

Install ik plugin

    su - lanjing
    cd /data/elasticsearch-5.0.1/ik
    mkdir ik
    logout
    cp /opt/elasticsearch-analysis-ik/target/releases/elasticsearch-analysis-ik-5.0.1.zip cd /data/elasticsearch-5.0.1/ik
    chown -R w.w /data/elasticsearch-5.0.1/plugins/ik/elasticsearch-analysis-ik-5.0.1.zip
    su - lanjing
    cd /data/elasticsearch-5.0.1/ik
    unzip elasticsearch-analysis-ik-5.0.1.zip
    
restart elasticsearch

## test
create index

    curl -u elastic:qwer1234 -XPUT http://localhost:9200/index
    
2.create a mapping

    curl -u elastic:qwer1234 -XPOST http://localhost:9200/index/fulltext/_mapping -d'
    {
        "fulltext": {
                 "_all": {
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word",
                "term_vector": "no",
                "store": "false"
            },
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_max_word",
                    "include_in_all": "true",
                    "boost": 8
                }
            }
        }
    }'

3.index some docs

    curl -u elastic:qwer1234 -XPOST http://localhost:9200/index/fulltext/1 -d'
    {"content":"美国留给伊拉克的是个烂摊子吗"}
    '
    
    curl -u elastic:qwer1234 -XPOST http://localhost:9200/index/fulltext/2 -d'
    {"content":"公安部：各地校车将享最高路权"}
    '
    
    curl -u elastic:qwer1234 -XPOST http://localhost:9200/index/fulltext/3 -d'
    {"content":"中韩渔警冲突调查：韩警平均每天扣1艘中国渔船"}
    '
    
    curl -u elastic:qwer1234 -XPOST http://localhost:9200/index/fulltext/4 -d'
    {"content":"中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首"}
    '

4.query with highlighting

    curl -u elastic:qwer1234 -XPOST http://localhost:9200/index/fulltext/_search  -d'
    {
        "query" : { "match" : { "content" : "中国" }},
        "highlight" : {
            "pre_tags" : ["<tag1>", "<tag2>"],
            "post_tags" : ["</tag1>", "</tag2>"],
            "fields" : {
                "content" : {}
            }
        }
    }
    '

Result

    {
        "took": 14,
        "timed_out": false,
        "_shards": {
            "total": 5,
            "successful": 5,
            "failed": 0
        },
        "hits": {
            "total": 2,
            "max_score": 2,
            "hits": [
                {
                    "_index": "index",
                    "_type": "fulltext",
                    "_id": "4",
                    "_score": 2,
                    "_source": {
                        "content": "中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首"
                    },
                    "highlight": {
                        "content": [
                            "<tag1>中国</tag1>驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首 "
                        ]
                    }
                },
                {
                    "_index": "index",
                    "_type": "fulltext",
                    "_id": "3",
                    "_score": 2,
                    "_source": {
                        "content": "中韩渔警冲突调查：韩警平均每天扣1艘中国渔船"
                    },
                    "highlight": {
                        "content": [
                            "均每天扣1艘<tag1>中国</tag1>渔船 "
                        ]
                    }
                }
            ]
        }
    }