# Analysis
确切值(exact values)及全文文本(full text)

    GET /_search?q=2014              # 12 个结果
    GET /_search?q=2014-09-15        # 还是 12 个结果 !
    GET /_search?q=date:2014-09-15   # 1  一个结果
    GET /_search?q=date:2014         # 0  个结果 !

倒排索引 (inverted index)

    倒排索引由在文档中出现的唯一的单词列表,以及对于每个单词在文档中的位置组成

analysis

分析(analysis)是这样一个过程：

    首先，表征化一个文本块为适用于倒排索引单独的词(term)
    然后标准化这些词为标准形式，提高它们的“可搜索性”或“查全率”

分析器analyzer

    字符过滤器character filter: 字符过滤器能够去除HTML标记，或者转换"&"为"and"
    分词器tokenizer: 可以根据空格或逗号将单词分开
    表征过滤token filters: 
        可以修改词(例如将"Quick"转为小写),去掉词(停用词像"a"、"and"``"the"等等),或者增加词(同义词像"jump"和"leap")

标准分析器（elasticsearch默认）

    根据Unicode Consortium的定义的单词边界(word boundaries)来切分文本，然后去掉大部分标点符号。最后，把所有词转为小写

简单分析器

    将非单个字母的文本切分，然后把每个词转为小写

空格分析器

    空格分析器依据空格切分文本。它不转换小写

语言分析器

    例如，english分析器自带一套英语停用词库——像and或the这些与语义无关的通用词

当分析器被使用

    当你查询全文(full text)字段，查询将使用相同的分析器来分析查询字符串，以产生正确的词列表。
    当你查询一个确切值(exact value)字段，查询将不分析查询字符串，但是你可以自己指定

测试分析器

    GET /_analyze?analyzer=standard 
    { Text to analyze }

# Map   索引中每个文档都有一个类型(type)每个类型拥有自己的映射(mapping)
查看映射

    GET /gb/_mapping/tweet
    GET /megacorp/_mapping/employee

对于string字段，两个最重要的映射参数是index和analyer

index参数控制字符串以何种方式被索引。它包含以下三个值当中的一个：

    值              解释
    analyzed        首先分析这个字符串，然后索引。换言之，以全文形式索引此字段。
    not_analyzed    索引这个字段，使之可以被搜索，但是索引内容和指定值一样。不分析此字段。
    no              不索引这个字段。这个字段不能为搜索到。
    string类型字段默认值是analyzed。如果我们想映射字段为确切值，我们需要设置它为not_analyzed
    其他简单类型——long、double、date等等——也接受index参数，但相应的值只能是no和not_analyzed

分析

    对于analyzed类型的字符串字段，使用analyzer参数来指定哪一种分析器将在搜索和索引的时候使用
    {
        "about": {
            "type":     "string",
            "analyzer": "english"
        }
    }

example

    PUT /gb
    {
      "mappings": {
        "tweet" : {
          "properties" : {
            "tweet" : {
              "type" :    "string",
              "analyzer": "english"
            },
            "date" : {
              "type" :   "date"
            },
            "name" : {
              "type" :   "string"
            },
            "user_id" : {
              "type" :   "long"
            }
          }
        }
      }
    }
    
    PUT /gb/_mapping/tweet
    {
      "properties" : {
        "tag" : {
          "type" :    "string",
          "index":    "not_analyzed"
        }
      }
    }
    
    GET /gb/_analyze?field=tweet 
    { Black-cats }
    
    GET /gb/_analyze?field=tag 
    { Black-cats }
