#!/bin/bash

[ -d /data ] || mkdir /data

consul agent -server -bootstrap -data-dir /data/consul -bind=0.0.0.0 >/var/log/consul.log 2>&1 &

echo 'DOCKER_OPTS="--kv-store=consul:localhost:8500 --label=com.docker.network.driver.overlay.bind_interface=eth0 --default-network=overlay:multihost"' > /etc/default/docker

#restart docker
service docker restart
