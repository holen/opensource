# Install elasticseach on Centos6.6
##Download elasticsearch

    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.0.1.tar.gz

##Require(https://www.elastic.co/guide/en/elasticsearch/reference/current/setting-system-settings.html#sysconfig)
  
vim /etc/security/limits.conf

    * soft nofile 65536
    * hard nofile 65536
    lanjing - memlock unlimited

vim /etc/security/limits.d/90-nproc.conf

    # Default limit for number of user's processes to prevent
    *          soft    nproc     65535
    root       soft    nproc     unlimited

vim /etc/sysctl.conf

    vm.max_map_count=262144
    vm.swappiness = 1

command

    swapoff -a
    sysctl  -p

Create a user to start elasticsearch

    useradd -d /home/lanjing lanjing

##Run elasticsearch

    tar zxvf elasticsearch-5.0.1.tar.gz
    mv elasticsearch-5.0.1 /data/
    chown -R lanjing.lanjing /data/elasticsearch-5.0.1
    su - lanjing
    cd /data/elasticsearch-5.0.1
    ./bin/elasticsearch -d -p pid

##Configure elasticsearch
cat /data/elasticsearch-5.0.1/config/elasticsearch.yml | grep -v '^#'

    cluster.name: lanjing
    node.name: node1
    node.attr.rack: r1
    bootstrap.memory_lock: true
    path.data: /data/elasticsearch-5.0.1/data
    path.logs: /data/elasticsearch-5.0.1/logs
    network.host: 0.0.0.0
    http.port: 9200
    gateway.recover_after_nodes: 1

vim /data/elasticsearch-5.0.1/config/jvm.options # heap size no more than 50% of physical RAM

    -Xms2g
    -Xmx2g

## Test
curl -XGET 'localhost:9200/?pretty'

    {
      "name" : "node1",
      "cluster_name" : "holen",
      "cluster_uuid" : "TDxoCSReQ6q6ueYvDXg4Mg",
      "version" : {
        "number" : "5.0.1",
        "build_hash" : "080bb47",
        "build_date" : "2016-11-11T22:08:49.812Z",
        "build_snapshot" : false,
        "lucene_version" : "6.2.1"
      },
      "tagline" : "You Know, for Search"
    }

## Cluster Health

GET /_cat/health?v

##  list of nodes in our cluster

GET /_cat/nodes?v

## List All Indices

GET /_cat/indices?v

## Create an Index

PUT /customer?pretty
GET /_cat/indices?v

## Index and Query a Document
Let’s index a simple customer document into the customer index, "external" type, with an ID of 1 as follows:

    PUT /customer/external/1?pretty
    {
          "name": "John Doe"
    }

Query

    GET /customer/external/1?pretty

## Delete an Index
Now let’s delete the index that we just created and then list all the indexes again:

    DELETE /customer?pretty
    GET /_cat/indices?v

## Update Document

    POST /customer/external/1/_update?pretty
    {
          "doc": { "name": "Jane Doe", "age": 20 }
    }

##Deleting Documents
Deleting a document is fairly straightforward. This example shows how to delete our previous customer with the ID of 2:

    DELETE /customer/external/2?pretty

## Batch process

    POST /customer/external/_bulk?pretty
    {"index":{"_id":"1"}}
    {"name": "John Doe" }
    {"index":{"_id":"2"}}
    {"name": "Jane Doe" }

    POST /customer/external/_bulk?pretty
    {"update":{"_id":"1"}}
    {"doc": { "name": "John Doe becomes Jane Doe" } }
    {"delete":{"_id":"2"}}

## Exploring Your Data
Now that we’ve gotten a glimpse of the basics, let’s try to work on a more realistic dataset. I’ve prepared a sample of fictitious JSON documents of customer bank account information. Each document has the following schema:

	{
	    "account_number": 0,
	    "balance": 16623,
	    "firstname": "Bradshaw",
	    "lastname": "Mckenzie",
	    "age": 29,
	    "gender": "F",
	    "address": "244 Columbus Place",
	    "employer": "Euron",
	    "email": "bradshawmckenzie@euron.com",
	    "city": "Hobucken",
	    "state": "CO"
	}

Extract it to our current directory and let’s load it into our cluster as follows:

	curl -XPOST 'localhost:9200/bank/account/_bulk?pretty&refresh' --data-binary "@accounts.json"
	curl 'localhost:9200/_cat/indices?v'

## Search API

	GET /bank/_search
	{
	  "query": { "match_all": {} },
	  "sort": [
	    { "account_number": "asc" }
	  ]
	}

