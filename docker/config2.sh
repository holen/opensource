#!/bin/bash

[ -d /data ] || mkdir /data

consul agent -data-dir /data/consul -bind=0.0.0.0 >/var/log/consul.log 2>&1 &

sleep 2

consul join $IP

cat <<-EOS > /etc/default/docker
DOCKER_OPTS="--kv-store=consul:localhost:8500 --label=com.docker.network.driver.overlay.bind_interface=eth0 --label=com.docker.network.driver.overlay.neighbor_ip=$IP --default-network=overlay:multihost"
EOS

#restart docker
service docker restart
