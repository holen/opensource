# data (object, json)
metadata

    _index  文档存储的地方
    _type   文档代表的对象的类
    _id     文档的唯一标识

index

    PUT /website/blog/123
    {
      "title": "My first blog entry",
      "text":  "Just trying this out...",
      "date":  "2014/01/01"
    }

    POST /website/blog/
    {
      "title": "My second blog entry",
      "text":  "Still trying this out...",
      "date":  "2014/01/01"
    }

Get

    GET /website/blog/123?pretty
    curl -i -XGET http://localhost:9200/website/blog/124?pretty
    GET /website/blog/123?_source=title,text
    GET /website/blog/123/_source

Exist

    curl -i -XHEAD http://localhost:9200/website/blog/123
   
Update

    PUT /website/blog/123
    {
      "title": "My first blog entry",
      "text":  "I am starting to get the hang of this...",
      "date":  "2014/01/02"
    }

Create 

    PUT /website/blog/123?op_type=create
    PUT /website/blog/123/_create

Delete

    DELETE /website/blog/123

版本控制,检查_version是否与请求中指定的一致

    PUT /website/blog/1?version=1
    {
      "title": "My first blog entry",
      "text":  "Starting to get the hang of this..."
    }

外部版本控制,检查是否小于指定的版本

    PUT /website/blog/2?version=5&version_type=external

mget

    GET /_mget
    {
       "docs" : [
          {
             "_index" : "website",
             "_type" :  "blog",
             "_id" :    2
          },
          {
             "_index" : "website",
             "_type" :  "pageviews",
             "_id" :    1,
             "_source": "views"
          }
       ]
    }

    GET /website/blog/_mget
    {
       "docs" : [
          { "_id" : 2 },
          { "_type" : "pageviews", "_id" :   1 }
       ]
    }

    GET /website/blog/_mget
    {
       "ids" : [ "2", "1" ]
    }


