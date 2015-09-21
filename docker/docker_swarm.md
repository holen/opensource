# Install docker swarm 
https://docs.docker.com/swarm/install-manual/  

Host1(manage, node1):

    docker pull swarm

    docker run --rm swarm create # token_id
    
    vim /etc/default/docker
    DOCKER_OPTS="--insecure-registry=0.0.0.0/0 -H 0.0.0.0:2375 -H unix:///var/run/docker.sock --label label_name=docker1"

    service docker restart 

    docker run -d -p 2376:2375 swarm manage token://token_id

    docker ps -a 

    docker -H host1_ip:2376 info

    docker run -d swarm join --addr=host1_ip:2375 token://token_id

    docker -H host1_ip:2376 ps
    docker -H host1_ip:2376 images

    docker -H host1_ip:2376 run -it --name busybox -e constraint:label_name==docker2 busybox

Host2(node2):

    vim /etc/default/docker
    DOCKER_OPTS="--insecure-registry=0.0.0.0/0 -H 0.0.0.0:2375 -H unix:///var/run/docker.sock --label label_name=docker2"

    service docker restart
    ps -aux | grep docker

    docker run -d swarm join --addr=host2_ip:2375 token://token_id

####  docker swarm scheduler

filter:  
https://docs.docker.com/swarm/scheduler/filter/  
    
    Constraint约束
    Affinity亲和性
    Port
    Dependency
    Health

Weith:  
https://docs.docker.com/swarm/scheduler/strategy/  
    
    Spread最少
    Binpack最多
    Random
