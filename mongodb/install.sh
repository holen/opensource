#!/bin/bash

apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
cat /etc/apt/sources.list.d/mongodb.list 
apt-get update
# apt-get install mongodb-10gen -y
apt-get install mongodb-org mongodb-org-server mongodb-org-shell mongodb-org-mongos mongodb-org-tools
