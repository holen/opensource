# Docker 网络管理  

# NAT
    
    docker run -it --name csphere-nat busybox sh
    iptables -L -n -t nat
    docer run -it -p 2222:22 --name csphere-nat2 busybox sh
    iptables -L -n -t nat 

# Host

    docker run -it --name csphere-host --net=host csphere sh

# Other container (共享container的网络模式)
    
    docker run -it --name csphere busybox sh
    docker run -it --name csphere-con --net=container:csphere busybox sh

# none (无网络配置)

    docker run -it --name csphere-none --net=none busybox sh 

# Delete all container

    docker rm -f $(docker ps -a -q)

# overlay (跨主机通信)

Host1:

    ./config1.sh     
    consul members

    docker run -it --name test1 busybox sh

Host2:
    IP=host1_IP ./config2.sh
    consul members

    docker run -it --name test2 busybox sh    
    ping test1
    cat /etc/hosts

# 

    docker network ls
    docker service ls
    docker service help
    docker service publish test-bridge.bridge
    docker service attach test1 test-bridge.bridge
    docker exec -it sh
