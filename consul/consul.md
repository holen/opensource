# Introduction

    It is a tool for discovering and configuring services in your infrastructure.

# Install 

    wget https://dl.bintray.com/mitchellh/consul/0.5.2_linux_amd64.zip
    unzip 0.5.2_linux_amd64.zip
    cp consul /usr/local/bin/

# Run agent 

    consul agent -server -bootstrap-expect 1 -data-dir /tmp/consul
    consul members
    curl localhost:8500/v1/catalog/nodes
    dig @127.0.0.1 -p 8600 Armons-MacBook-Air.node.consul

# Registry service 

    mkdir /etc/consul.d
    echo '{"service": {"name": "web", "tags": ["rails"], "port": 80}}' > /etc/consul.d/web.json
    consul agent -server -bootstrap-expect 1 -data-dir /tmp/consul -config-dir /etc/consul.d
    dig @127.0.0.1 -p 8600 web.service.consul
    dig @127.0.0.1 -p 8600 web.service.consul SRV
    dig @127.0.0.1 -p 8600 rails.web.service.consul
    curl http://localhost:8500/v1/catalog/service/web

# Consul cluster
start agent

    vagrant@n1:~$ consul agent -server -bootstrap-expect 1 -data-dir /tmp/consul -node=agent-one -bind=172.20.20.10
    vagrant@n2:~$ consul agent -data-dir /tmp/consul -node=agent-two -bind=172.20.20.11

join cluster 

    vagrant@n1:~$ consul join 172.20.20.11

query nodes

    vagrant@n1:~$ dig @127.0.0.1 -p 8600 agent-two.node.consul

# Health check 
server

    consul agent -server -bootstrap-expect 1 -data-dir /tmp/consul -node=agent-one -bind=172.20.20.10 -config-dir /etc/consul.d/ & 

client

    consul agent -data-dir /tmp/consul -node=agent-two -bind=172.20.20.11 &
    echo '{"service": {"name": "web", "tags": ["rails"], "port": 80, "check": {"script": "curl localhost >/dev/null 2>&1", "interval": "10s"}}}' > /etc/consul.d/web.jsion
    echo '{"check": {"name": "ping", "script": "ping -c1 baidu.com > /dev/null", "interval": "30s"}}' > /etc/consul.d/ping.json
   
check health

    curl http://localhost:8500/v1/health/state/critical
    dig @127.0.0.1 -p 8600 web.service.consul

# KEY/VALUE DATA
add k/v

    curl -v http://localhost:8500/v1/kv/?recurse
    curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/key1
    curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/key2?flags=42
    curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/sub/key3
    curl http://localhost:8500/v1/kv/?recurse
    curl http://localhost:8500/v1/kv/web/key1

delete k/v

    curl -X DELETE http://localhost:8500/v1/kv/web/sub?recurse
    curl http://localhost:8500/v1/kv/?recurse

modify k/v

    curl -X PUT -d 'newval' http://localhost:8500/v1/kv/web/key1?cas=97
    curl -X PUT -d 'newval' http://localhost:8500/v1/kv/web/key1?cas=97
    curl "http://localhost:8500/v1/kv/web/key2?index=101&wait=5s"
