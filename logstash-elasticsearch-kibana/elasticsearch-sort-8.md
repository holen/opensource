# sort
field sort

    GET /_search
    {
        "query" : {
            "filtered" : {
                "filter" : { "term" : { "user_id" : 1 }}
            }
        },
        "sort": { "date": { "order": "desc" }}
    }

为多值字段排序

    "sort": {
        "dates": {
            "order": "asc",
            "mode":  "min"
        }
    }

多值字段字符串排序

    "tweet": { 
        "type":     "string",
        "analyzer": "english",
        "fields": {
            "raw": { 
                "type":  "string",
                "index": "not_analyzed"
            }
        }
    }

tweet 字段用于全文本的 analyzed 索引方式不变。

新增的 tweet.raw 子字段索引方式是 not_analyzed。

现在，在给数据重建索引后，我们既可以使用 tweet 字段进行全文本搜索，也可以用tweet.raw字段进行排序：

    GET /_search
    {
        "query": {
            "match": {
                "tweet": "elasticsearch"
            }
        },
        "sort": "tweet.raw"
    }

# 相关性
ElasticSearch的相似度算法被定义为 TF/IDF，即检索词频率/反向文档频率，包括一下内容：  

检索词频率

    检索词在该字段出现的频率？出现频率越高，相关性也越高。 字段中出现过5次要比只出现过1次的相关性高。

反向文档频率

    每个检索词在索引中出现的频率？频率越高，相关性越低。 检索词出现在多数文档中会比出现在少数文档中的权重更低， 即检验一个检索词在文档中的普遍重要性。

字段长度准则::

    字段的长度是多少？长度越长，相关性越低。 检索词出现在一个短的 title 要比同样的词出现在一个长的 content 字段

理解评分标准 _score

    GET /_search?explain
    {
       "query"   : { "match" : { "tweet" : "honeymoon" }}
    }

# 数据字段
为了提高排序效率，ElasticSearch 会将所有字段的值加载到内存中，这就叫做"数据字段"

ElasticSearch中的字段数据常被应用到以下场景：

    对一个字段进行排序
    对一个字段进行聚合
    某些过滤，比如地理位置过滤
    某些与字段相关的脚本计算

