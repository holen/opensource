# Docker
## Install
install on ubuntu12.04.3

    apt-get install apt-transport-https
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
    sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"

    apt-get update
    apt-get install lxc-docker
    docker run -i -t ubuntu /bin/bash
    #上边的命令会自动下载ubuntu镜像，并且会在容器内执行bash,输入exit来退出
    docker pull ubuntu #下载ubuntu镜像

test run

    docker run -i -t ubuntu /bin/bash 

access container 

    # install nsenter
    wget https://www.kernel.org/pub/linux/utils/util-linux/v2.25/util-linux-2.25.tar.gz
    tar zxvf util-linux-2.25.tar.gz 
    cd util-linux-2.25
    less README
    ./configure 
    make
    make install
    docker ps -a
    # get container pid
    docker inspect --format "{{ .State.Pid }}" container-id
    # access container 
    nsenter --target $pid --mount --uts --ipc --net --pid

连接container

    docker run -link redis:db -i -t ubuntu:12.04 /bin/bash

create image

    docker build --tag my/repo /data/Dockerfile

push images to Docker Hub

    docker login
    docker push my/repo

run images

    docker run --name <name for container> -d my/repo --noprealloc --smallfiles

##更新提交镜像

    docker run -t -i ubuntu /bin/bash 
    docker commit -m="Add ssh" -a="holen" cfa69f9daf45 ubuntu:v2

##管理容器数据
添加一个数据卷

    docker run -d -P --name web -v /webapp training/webapp python app.python

挂载一个主机目录作为卷

    docker run -d -P --name web -v /src/webapp:/opt/webapp training/webapp python app.py

创建一个挂在数据卷的容器

    docker run -d -v /dbdata --name dbdata training/postgres
    docker run -d --volumes-from dbdata --name db1 training/postgres
    docker run -d --volumes-from dbdata --name db2 training/postgres

##自定义 Linux 网桥
如果你想自定义网桥，你可以执行以下步骤。你可以在这个网桥后面分配一个子网，并为这个子网分配地址。下面的命令会为 Docker 子网分配 10.0.0.0/24 地址段：

    $ apt-get install bridge-utils
    $ brctl addbr br0
    $ ifconfig br0 10.0.0.1 netmask 255.255.255.0

然后在 /etc/default/docker.io 文件的 DOCKER\_OPTS 变量里添加“-b=br0”选项，并重启 Docker 服务：

    $ service docker.io restart
    $ docker -d -b="bridge0" >> /var/log/docker.log 2>&1 &

到目前为止，任何创建的容器都会连上 br0 网桥，它们的 IP 地址会从 10.0.0.0/24 中自动分配（译注：在10.0.0.2到10.0.0.254之间随机分配）。 

## 参考文献
[docker 英文文档](https://docs.docker.com/articles/networking/#bridge-building)  
[docker中文文档](http://www.widuu.com/chinese_docker/userguide/README.html)  
[在 Ubuntu 中用 Docker 管理 Linux Container 容器](http://linux.cn/article-3139-1.html)  
[如何进入Docker容器](http://www.oschina.net/translate/enter-docker-container)  
[为什么不需要在 Docker 容器中运行 sshd](http://www.oschina.net/translate/why-you-dont-need-to-run-sshd-in-docker?cmp)  
[在UOS上体验CoreOS](https://www.ustack.com/blog/running-coreos-on-uos/)  
