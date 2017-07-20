# filebeat 

## elastic install ingest plugin for Nginx module

    ./bin/elasticsearch-plugin install ingest-geoip
    ./bin/elasticsearch-plugin install ingest-user-agent

## Install Filebeat 

    curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-5.5.0-x86_64.rpm
    sudo rpm -vi filebeat-5.5.0-x86_64.rpm

## configure Filebeat 

    less filebeat.yml 
    filebeat.modules:
    - module: nginx
      access:
        enabled: true
        var.paths: ["/data/logs/access_*.log"]
      error:
        enabled: true
        var.paths: ["/data/logs/error_*.log"]
    output.elasticsearch:
      hosts: ["10.30.4.130:9200"]
      username: "elastic"
      password: "qianbitou2017"
      index: "filebeat-%{+yyyy.MM.dd}"
      template.enabled: true
      template.name: "filebeat"
      template.path: "${path.config}/filebeat.template.json"
      template.overwrite: true

## Loading the Template Manually

    curl -H 'Content-Type: application/json' -XPUT 'http://localhost:9200/_template/filebeat' -d@/etc/filebeat/filebeat.template.json

## check conf and start filebeat

    filebeat.sh -configtest  
    /etc/init.d/filebeat start

## loading the kibana index pattern

    /usr/share/filebeat/scripts/import_dashboards -es http://10.30.4.130:9200 -user elastic -pass qianbitou2017 -only-index
