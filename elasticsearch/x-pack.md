#X-pack
## [Install X-pack plugin](https://www.elastic.co/guide/en/x-pack/current/installing-xpack.html)
Install X-Pack into Elasticsearch

    bin/elasticsearch-plugin install x-pack

vim elasticsearch.yml

    action.auto_create_index: .security,.monitoring*,.watches,.triggered_watches,.watcher-history*

Start Elasticsearch

    bin/elasticsearch -d -p pid

Install X-Pack into Kibana

    bin/kibana-plugin install x-pack
    bin/kibana-plugin install file:///path/to/file/x-pack-5.0.1.zip

Start Kibana

    bin/kibana &


Navigate to Kibana at http://localhost:5601/

Log in as the built-in elastic user with the password changeme.

##[Getting Started with Security](https://www.elastic.co/guide/en/x-pack/current/security-getting-started.html)
Change the passwords of the built in kibana and elastic users:

    curl -XPUT -u elastic 'localhost:9200/_xpack/security/user/elastic/_password' -d '{
      "password" : "elasticpassword"
    }'

    curl -XPUT -u elastic 'localhost:9200/_xpack/security/user/kibana/_password' -d '{
      "password" : "kibanapassword"
    }'

 Set up roles and users to control access to Elasticsearch and Kibana. For example, to grant John Doe full access to all indices that match the pattern events* and enable him to create visualizations and dashboards for those indices in Kibana, you could create an events_admin role and and assign the role to a new johndoe user.

    curl -XPOST -u elastic 'localhost:9200/_xpack/security/role/events_admin' -d '{
      "indices" : [
        {
          "names" : [ "events*" ],
          "privileges" : [ "all" ]
        },
        {
          "names" : [ ".kibana*" ],
          "privileges" : [ "manage", "read", "index" ]
        }
      ]
    }'

    {"role":{"created":true}}

    curl -XPOST -u elastic 'localhost:9200/_xpack/security/user/johndoe' -d '{
      "password" : "userpassword",
      "full_name" : "John Doe",
      "email" : "john.doe@anony.mous",
      "roles" : [ "events_admin" ]
    }'

    {"user":{"created":true}}

 Enable message authentication to verify that messages are not tampered with or corrupted in transit:

    Run the syskeygen tool from ES_HOME without any options:
    bin/x-pack/syskeygen

    This creates a system key file in CONFIG_DIR/x-pack/system_key.
    Copy the generated system key to the rest of the nodes in the cluster.
    scp 192.168.70.29:/data/elasticsearch-5.0.1/config/x-pack/system_key .

 Enable Auditing to keep track of attempted and successful interactions with your Elasticsearch cluster:

    Add the following setting to elasticsearch.yml on all nodes in your cluster:
    xpack.security.audit.enabled: true
    Restart Elasticsearch.

## [Getting Started with Monitoring](https://www.elastic.co/guide/en/x-pack/current/monitoring-getting-started.html)

    http://localhost:5601/

## [Getting Started with Alerting and Notification](https://www.elastic.co/guide/en/x-pack/current/watcher-getting-started.html)
Verify that Watcher is enabled

    curl -XGET -u elastic:changeme "http://localhost:9200/_xpack/watcher/stats"

[Watch Log Data for Errors](https://www.elastic.co/guide/en/x-pack/current/watch-log-data.html)

[Watch Your Cluster Health](https://www.elastic.co/guide/en/x-pack/current/watch-cluster-status.html)

    curl -XPUT -u elastic:changeme "localhost:9200/_xpack/watcher/watch/cluster_health_watch" -d '
    {
      "trigger" : {
        "schedule" : { "interval" : "10s" }
      },
      "input" : {
        "http" : {
          "request" : {
           "host" : "localhost",
           "port" : 9200,
           "path" : "/_cluster/health"
          }
        }
      },
      "condition" : {
        "compare" : {
          "ctx.payload.status" : { "eq" : "red" }
        }
      },
      "actions" : {
        "send_email" : {
          "email" : {
            "to" : "zhl@linggan.com",
            "subject" : "Env: Test! Cluster Status Warning",
            "body" : "Cluster status is RED"
          }
        }
      }
    }'
