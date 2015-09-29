# index manage
create index

    PUT /my_index
    {
        "settings": { ... any settings ... },
        "mappings": {
            "type_one": { ... any mappings ... },
            "type_two": { ... any mappings ... },
            ...
    }

delete index

    DELETE /my_index
    DELETE /index_one,index_two
    DELETE /index_*
    DELETE /_all

setting index

    PUT /my_temp_index
    {
        "settings": {
            "number_of_shards" :   1,
            "number_of_replicas" : 0
        }
    }
    
    PUT /my_temp_index/_settings
    {
        "number_of_replicas": 1
    }

配置分析器

    PUT /spanish_docs
    {
        "settings": {
            "analysis": {
                "analyzer": {
                    "es_std": {
                        "type":      "standard",
                        "stopwords": "_spanish_"
                    }
                }
            }
        }
    }

    GET /spanish_docs/_analyze?analyzer=es_std
    El veloz zorro marrón

创建自定义分析器

    PUT /my_index
    {
        "settings": {
            "analysis": {
                "char_filter": { ... custom character filters ... },
                "tokenizer":   { ...    custom tokenizers     ... },
                "filter":      { ...   custom token filters   ... },
                "analyzer":    { ...    custom analyzers      ... }
            }
        }
    }

我们来配置一个这样的分析器：  
用 html_strip 字符过滤器去除所有的 HTML 标签, 将 & 替换成 and，使用一个自定义的 mapping 字符过滤器

    "char_filter": {
        "&_to_and": {
            "type":       "mapping",
            "mappings": [ "&=> and "]
        }
    }

使用 standard 分词器分割单词,使用 lowercase 表征过滤器将词转为小写,用 stop 表征过滤器去除一些自定义停用词。

    "filter": {
        "my_stopwords": {
            "type":        "stop",
            "stopwords": [ "the", "a" ]
        }
    }

根据以上描述来将预定义好的分词器和过滤器组合成我们的分析器：

    "analyzer": {
        "my_analyzer": {
            "type":           "custom",
            "char_filter":  [ "html_strip", "&_to_and" ],
            "tokenizer":      "standard",
            "filter":       [ "lowercase", "my_stopwords" ]
        }
    }

用下面的方式可以将以上请求合并成一条：

    PUT /my_index
    {
        "settings": {
            "analysis": {
                "char_filter": {
                    "&_to_and": {
                        "type":       "mapping",
                        "mappings": [ "&=> and "]
                }},
                "filter": {
                    "my_stopwords": {
                        "type":       "stop",
                        "stopwords": [ "the", "a" ]
                }},
                "analyzer": {
                    "my_analyzer": {
                        "type":         "custom",
                        "char_filter":  [ "html_strip", "&_to_and" ],
                        "tokenizer":    "standard",
                        "filter":       [ "lowercase", "my_stopwords" ]
                }}
    }}}

创建索引后，用 analyze API 来测试新的分析器：

    GET /my_index/_analyze?analyzer=my_analyzer
    The quick & brown fox

下面的结果证明我们的分析器能正常工作了：

    {
      "tokens" : [
          { "token" :   "quick",    "position" : 2 },
          { "token" :   "and",      "position" : 3 },
          { "token" :   "brown",    "position" : 4 },
          { "token" :   "fox",      "position" : 5 }
        ]
    }

除非我们告诉 Elasticsearch 在哪里使用，否则分析器不会起作用。我们可以通过下面的映射将它应用在一个 string 类型的字段上：

    PUT /my_index/_mapping/my_type
    {
        "properties": {
            "title": {
                "type":      "string",
                "analyzer":  "my_analyzer"
            }
        }
    }

# 根对象
映射的最高一层被称为 根对象，它可能包含下面几项：

    一个 properties 节点，列出了文档中可能包含的每个字段的映射
    多个元数据字段，每一个都以下划线开头，例如 _type, _id 和 _source
    设置项，控制如何动态处理新的字段，例如 analyzer, dynamic_date_formats 和 dynamic_templates。
    其他设置，可以同时应用在根对象和其他 object 类型的字段上，例如 enabled, dynamic 和 include_in_all

属性

    type： 字段的数据类型，例如 string 和 date
    index： 字段是否应当被当成全文来搜索（analyzed），或被当成一个准确的值（not_analyzed），还是完全不可被搜索（no）
    analyzer： 确定在索引和或搜索时全文字段使用的 分析器。

# 元数据中的ID 字段
文档唯一标识由四个元数据字段组成：

    _id：文档的字符串 ID
    _type：文档的类型名
    _index：文档所在的索引
    _uid：_type 和 _id 连接成的 type#id

默认情况下，_uid 是被保存（可取回）和索引（可搜索）的。_type 字段被索引但是没有保存，_id 和 _index 字段则既没有索引也没有储存，它们并不是真实存在的

# 动态映射
你可以通过 dynamic 设置来控制这些行为，它接受下面几个选项：

    true：自动添加字段（默认）
    false：忽略字段
    strict：当遇到未知字段时抛出异常

example

    PUT /my_index
    {
        "mappings": {
            "my_type": {
                "dynamic":      "strict",
                "properties": {
                    "title":  { "type": "string"},
                    "stash":  {
                        "type":     "object",
                        "dynamic":  true
                    }
                }
            }
        }
    }

# 默认映射
我们可以使用 _default_ 映射对所有类型禁用 _all 字段，而只在 blog 字段上开启它：

    PUT /my_index
    {
        "mappings": {
            "_default_": {
                "_all": { "enabled":  false }
            },
            "blog": {
                "_all": { "enabled":  true  }
            }
        }
    }

_default_ 映射也是定义索引级别的动态模板的好地方

# 别名
索引 别名 就像一个快捷方式或软连接，可以指向一个或多个索引，也可以给任何需要索引名的 API 使用,允许我们做到

    在一个运行的集群上无缝的从一个索引切换到另一个
    给多个索引分类（例如，last_three_months）
    给索引的一个子集创建 视图

create alias

    DELETE /my_index
    PUT /my_index_v1
    PUT /my_index_v1/_alias/my_index

show alias

    GET /*/_alias/my_index
    GET /my_index_v1/_alias/*

create a empty index

    PUT /my_index_v2
    {
        "mappings": {
            "my_type": {
                "properties": {
                    "tags": {
                        "type":   "string",
                        "index":  "not_analyzed"
                    }
                }
            }
        }
    }

move my_index_v1 to my_index_v2
    
    POST /_aliases
    {
        "actions": [
            { "remove": { "index": "my_index_v1", "alias": "my_index" }},
            { "add":    { "index": "my_index_v2", "alias": "my_index" }}
        ]
    }
