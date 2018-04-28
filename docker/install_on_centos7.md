# 安装Docker
ref: http://docs.docker-cn.com/engine/installation/linux/docker-ce/centos/  

操作系统要求

    如需安装 Docker CE，您需要 64 位版本的 CentOS 7。

卸载旧版本

   $ sudo yum remove docker docker-common docker-selinux docker-engine 

安装所需的软件包

	$ sudo yum install -y yum-utils device-mapper-persistent-data lvm2

使用下列命令设置 stable 镜像仓库

	 $ sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

更新 yum 软件包索引

	$ sudo yum makecache fast

安装最新版本的 Docker CE

	$ sudo yum install docker-ce

安装特定版本的Docker CE

	[root@iZ94g3nv876Z ~]# yum list docker-ce.x86_64 --showduplicates | sort -r
	 * updates: mirrors.aliyuncs.com
	Loading mirror speeds from cached hostfile
	Loaded plugins: fastestmirror
	 * extras: mirrors.aliyuncs.com
	 * epel: mirrors.aliyuncs.com
	docker-ce.x86_64            18.03.0.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.12.1.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.12.0.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.09.1.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.09.0.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.06.2.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.06.1.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.06.0.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.03.2.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.03.1.ce-1.el7.centos             docker-ce-stable
	docker-ce.x86_64            17.03.0.ce-1.el7.centos             docker-ce-stable
	$ sudo yum install docker-ce-<VERSION>
	[root@iZ94g3nv876Z ~]# yum install docker-ce-18.03.0.ce-1.el7.centos

启动 Docker

    $ sudo systemctl start docker

运行 hello-world 镜像

    $ sudo docker run hello-world
    $ docker --version

# 使用Dockerfile运行容器应用
ref: http://docs.docker-cn.com/get-started/part2/  

构建应用

    # 文件在 get_start 里面
    [root@iZ94g3nv876Z get_start]# ls
    app.py  Dockerfile  requirements.txt

    docker build -t friendlyhello .

查看构建的镜像

    $ docker images

运行应用

    docker run -d -p 4000:80 friendlyhello

测试应用

    [root@iZ94g3nv876Z get_start]# curl http://localhost:4000
    <h3>Hello World!</h3><b>Hostname:</b> 9b01a675bcc1<br/><b>Visits:</b> <i>cannot connect to Redis, counter disabled</i>

使用 docker ps 查看缩写容器 ID

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED
    1fa4ab2cf395        friendlyhello       "python app.py"     28 seconds ago

    您将看到 CONTAINER ID 与 http://localhost:4000 上的内容相匹配。
    现在，使用 docker stop 及 CONTAINER ID 结束该进程，如下所示：
    docker stop 1fa4ab2cf395
    docker rm 1fa4ab2cf395

标记镜像

    docker tag friendlyhello zhl/get-started:v1
    docker images

此阶段的基本 Docker 命令列表，以及一些相关命令

    docker build -t friendlyname .          # 使用此目录的 Dockerfile 创建镜像
    docker run -p 4000:80 friendlyname      # 运行端口 4000 到 80 的friendlyname映射
    docker run -d -p 4000:80 friendlyname   # 内容相同，但是容器是运行在后台
    docker ps                               # 查看所有正在运行的容器的列表
    docker stop <hash>                      # 平稳地停止指定的容器
    docker ps -a                            # 查看所有容器的列表，甚至包含未运行的容器
    docker kill <hash>                      # 强制关闭指定的容器
    docker rm <hash>                        # 从此机器中删除指定的容器
    docker rm $(docker ps -a -q)            # 从此机器中删除所有容器
    docker images -a                        # 显示此机器上的所有镜像
    docker rmi <imagename>                  # 从此机器中删除指定的镜像
    docker rmi $(docker images -q)          # 从此机器中删除所有镜像
    docker login                            # 使用您的 Docker 凭证登录此 CLI 会话
    docker tag <image> username/repository:tag  # 标记 <image> 以上传到镜像库
    docker push username/repository:tag     # 将已标记的镜像上传到镜像库
    docker run username/repository:tag      # 运行镜像库中的镜像

# 运用docker-compose、swarm运行新的负载均衡的应用

始化一个群集(Swarm)

    docker swarm init --advertise-addr 192.168.120.201
    [root@localhost get_start]# docker swarm init 
    Swarm initialized: current node (mqc1fb5v57y5h5hwdd5up0es7) is now a manager.
    To add a worker to this swarm, run the following command:
        docker swarm join --token SWMTKN-1-2knv2mvhvzip96zb1oa4czcwtziaiqv3rziz2dmakk71k6y4do-av1ylsk68473era9e1plg9cno 192.168.120.201:2377
    To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

您必须为应用指定一个名称。在此处该名称设置为 getstartedlab, docker-compose.yml存在于 get_start 中：

    [root@localhost get_start]# docker stack deploy -c docker-compose.yml getstartedlab
    Creating network getstartedlab_webnet
    Creating service getstartedlab_web

查看您刚才启动的五个容器的列表

    [root@localhost get_start]# docker stack ps getstartedlab
    ID                  NAME                      IMAGE                NODE                    DESIRED STATE       CURRENT STATE                    ERROR   PORTS
    p6zbb5hd9z2n        getstartedlab_web.1       zhl/get-started:v1   localhost.localdomain   Running             Running less than a second ago                                 
    qprzg0whp734         \_ getstartedlab_web.1   zhl/get-started:v1   localhost.localdomain   Shutdown            Failed 6 seconds ago             "task: non-zero exit (137)"   
    oavklo7yux7j        getstartedlab_web.2       zhl/get-started:v1   localhost.localdomain   Running             Running 15 seconds ago                                         
    c0wzjs0bqdmi         \_ getstartedlab_web.2   zhl/get-started:v1   localhost.localdomain   Shutdown            Failed 21 seconds ago            "task: non-zero exit (137)"   

扩展应用

    您可以通过在 docker-compose.yml 中更改 replicas 值，保存更改并重新运行 docker stack deploy 命令来扩展应用：
    docker stack deploy -c docker-compose.yml getstartedlab
    docker stack ps

清除应用

    docker stack rm getstartedlab

我们的单节点 swarm 仍处于正常运行状态

    [root@localhost get_start]# docker node ls
    ID                            HOSTNAME                STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
    mqc1fb5v57y5h5hwdd5up0es7 *   localhost.localdomain   Ready               Active              Leader              18.03.0-ce

清除 swarm

    docker swarm leave --force 

此阶段探索的一些命令：

    docker stack ls                                 # 列出此 Docker 主机上所有正在运行的应用
    docker stack deploy -c <composefile> <appname>  # 运行指定的 Compose 文件
    docker stack services <appname>                 # 列出与应用关联的服务
    docker stack ps <appname>                       # 列出与应用关联的正在运行的容器
    docker stack rm <appname>                       # 清除应用

# Install docker-machine

Installing Machine Directly

    curl -L https://github.com/docker/machine/releases/download/v0.14.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
    chmod +x /tmp/docker-machine &&
    sudo cp /tmp/docker-machine /usr/local/bin/docker-machine

    [root@localhost ~]# docker-machine version
    docker-machine version 0.14.0, build 89b8332

Installing bash completion scripts

    wget https://raw.githubusercontent.com/docker/machine/master/contrib/completion/bash/docker-machine.bash
    wget https://raw.githubusercontent.com/docker/machine/master/contrib/completion/bash/docker-machine-prompt.bash
    wget https://raw.githubusercontent.com/docker/machine/master/contrib/completion/bash/docker-machine-wrapper.bash
	下载上面三个文件，复制到 /etc/bash_completion.d 或者 /usr/local/etc/bash_completion.d 目录

    add $(__docker_machine_ps1) to your PS1 setting in ~/.bashrc.
    PS1='[\u@\h \W$(__docker_machine_ps1)]\$ '

To uninstall Docker Machine:

    Remove the executable: rm $(which docker-machine)
    Optionally, remove the machines you created.
    To remove each machine individually: docker-machine rm <machine-name>
    To remove all machines: docker-machine rm -f $(docker-machine ls -q)

# swarm 集群
安装 KVM driver for docker-machine

    curl -L https://github.com/dhiltgen/docker-machine-kvm/releases/download/v0.10.0/docker-machine-driver-kvm-centos7 > /usr/local/bin/docker-machine-driver-kvm 
    chmod +x /usr/local/bin/docker-machine-driver-kvm
    By default docker-machine-kvm uses a boot2docker.iso as guest os for the kvm hypervisior. 
    https://github.com/boot2docker/boot2docker
    For using another image use the --kvm-boot2docker-url parameter.

创建集群,先创建两个vm,一个用作管理节点，一个用作工作节点

    $ docker-machine create --driver kvm myvm1
    $ docker-machine create --driver kvm myvm2

    [root@localhost ~]# docker-machine ls
    NAME    ACTIVE   DRIVER   STATE     URL                         SWARM   DOCKER        ERRORS
    myvm1   -        kvm      Running   tcp://192.168.42.76:2376            v18.04.0-ce   
    myvm2   -        kvm      Running   tcp://192.168.42.222:2376           v18.04.0-ce   

    [root@localhost ~]# docker-machine env myvm1
    export DOCKER_TLS_VERIFY="1"
    export DOCKER_HOST="tcp://192.168.42.76:2376"
    export DOCKER_CERT_PATH="/root/.docker/machine/machines/myvm1"
    export DOCKER_MACHINE_NAME="myvm1"
    # Run this command to configure your shell: 
    # eval $(docker-machine env myvm1)

将myvm1设置为管理节点，用于执行docker命令并对加入swarm的工作节点进行身份验证

    通过运行 docker-machine ls 来复制 myvm1 的 IP 地址
    [root@localhost ~]# docker-machine ssh myvm1 "docker swarm init --advertise-addr 192.168.42.76:2377"
    Swarm initialized: current node (n952psl4j2lhx1tp8a46h9eep) is now a manager.
    To add a worker to this swarm, run the following command:
    docker swarm join --token SWMTKN-1-3c9of4thl4s73ybpfuz7smfzvcpts6gcjg9htcg8iixbd68jw1-2cqd820pbc0jk3mtr2608lyr4 192.168.42.76:2377
    To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

让 myvm2 加入您的新 swarm 作为工作节点

    [root@localhost ~]# docker-machine ssh myvm2 "docker swarm join --token SWMTKN-1-3c9of4thl4s73ybpfuz7smfzvcpts6gcjg9htcg8iixbd68jw1-2cqd820pbc0jk3mtr2608lyr4 192.168.42.76:2377"     
    This node joined a swarm as a worker.

    [root@localhost ~]# docker-machine ssh myvm1 "docker node ls"
    ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
    n952psl4j2lhx1tp8a46h9eep *   myvm1               Ready               Active              Leader              18.04.0-ce
    n25opvvodifa97eoyaq6tfvk8     myvm2               Ready               Active                                  18.04.0-ce

在集群上部署应用

    docker-machine scp docker-compose.yml myvm1:~
    docker-machine ssh myvm1 "docker stack deploy -c docker-compose.yml getstartedlab"
    $ docker-machine ssh myvm1 "docker stack ps getstartedlab"

访问集群

    运行 docker-machine ls 以获取 VM 的 IP 地址，并在浏览器上访问其中一个地址，并按“刷新”
    请记住，为了使用 swarm 中的入口网络， 您需要在 swarm 节点之间开放以下端口， 然后再启用 swarm mode：
    端口 7946 TCP/UDP，用于容器网络发现。
    端口 4789 UDP，用于容器入口网络。
    只需再次运行 docker stack deploy 即可部署这些更改

您可以使用 docker stack rm 清除技术栈。例如：

    docker-machine ssh myvm1 "docker stack rm getstartedlab"

以下是与 swarm 进行交互时您可能会运行的命令：

    docker-machine create --driver virtualbox myvm1         # 创建 VM（Mac、Win7、Linux）
    docker-machine create -d hyperv --hyperv-virtual-switch "myswitch" myvm1 # Win10
    docker-machine env myvm1                                # 查看有关节点的基本信息
    docker-machine ssh myvm1 "docker node ls"               # 列出 swarm 中的节点
    docker-machine ssh myvm1 "docker node inspect <node ID>"        # 检查节点
    docker-machine ssh myvm1 "docker swarm join-token -q worker"   # 查看加入令牌
    docker-machine ssh myvm1                                # 打开与 VM 的 SSH 会话；输入“exit”以结束会话
    docker-machine ssh myvm2 "docker swarm leave"           # 使工作节点退出 swarm
    docker-machine ssh myvm1 "docker swarm leave -f"        # 使主节点退出，终止 swarm
    docker-machine start myvm1                              # 启动当前未运行的 VM
    docker-machine stop $(docker-machine ls -q)             # 停止所有正在运行的 VM
    docker-machine rm $(docker-machine ls -q)               # 删除所有 VM 及其磁盘镜像
    docker-machine scp docker-compose.yml myvm1:~           # 将文件复制到节点的主目录
    docker-machine ssh myvm1 "docker stack deploy -c <file> <app>"   # 部署应用

# Deploy a service to the swarm
ref: http://docs.docker-cn.com/engine/swarm/swarm-tutorial/deploy-service/  
Deploy a service to the swarm

    [root@localhost ~]# docker-machine ssh myvm1

    docker@myvm1:~$ docker service create --replicas 1 --name helloworld alpine ping docker.com
    nnlqqn7mlfigfsdb5l0ww746q
    overall progress: 1 out of 1 tasks 
    1/1: running   [==================================================>] 
    verify: Service converged 

    docker@myvm1:~$ docker service ls
    ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
    nnlqqn7mlfig        helloworld          replicated          1/1                 alpine:latest       

	docker@myvm1:~$ docker service inspect --pretty helloworld 		## display the details about a service in an easily readable format
	docker@myvm1:~$ docker service inspect helloworld				## To return the service details in json format, run the same command without the --pretty flag

	docker@myvm1:~$ docker service ps helloworld					## see which nodes are running the service
	ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE             ERROR                              PORTS
	jtusckx1s3k1        helloworld.1        alpine:latest       myvm2               Running             Running 5 minutes ago
	[root@localhost ~]# docker-machine ssh myvm2 "docker ps"		## see details about the container for the task
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
	52da23a816b7        alpine:latest       "ping docker.com"   7 minutes ago       Up 7 minutes                            helloworld.1.jtusckx1s3k1575ow7fxpkyyg

	docker@myvm1:~$ docker service scale helloworld=3				## Scale the service in the swarm
	helloworld scaled to 3
	overall progress: 3 out of 3 tasks 
	1/3: running   [==================================================>] 
	2/3: running   [==================================================>] 
	3/3: running   [==================================================>] 
	verify: Service converged 

	docker@myvm1:~$ docker service ps helloworld
	ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE             ERROR                              PORTS
	jtusckx1s3k1        helloworld.1        alpine:latest       myvm2               Running             Running 19 minutes ago                                       
	vlli3rek642h        helloworld.2        alpine:latest       myvm1               Running             Running 3 minutes ago                                        
	q55gclqyvmpe        helloworld.3        alpine:latest       myvm1               Running             Running 3 minutes ago 

	docker@myvm1:~$ docker ps
	CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
	32d667599422        alpine:latest       "ping docker.com"   3 minutes ago       Up 3 minutes                            helloworld.2.vlli3rek642hdwv0xgyhwj5pt
	6f38c758debc        alpine:latest       "ping docker.com"   3 minutes ago       Up 3 minutes                            helloworld.3.q55gclqyvmpecdhv5v2l4tfed

	docker@myvm1:~$ docker service rm helloworld 				##  remove the helloworld service
	helloworld

Apply rolling updates to a service

Deploy Redis 3.0.6 to the swarm and configure the swarm with a 10 second update delay

	$ docker service create \
	  --replicas 3 \
	  --name redis \
	  --update-delay 10s \
	  redis:3.0.6
	## The --update-delay flag configures the time delay between updates to a service task or sets of tasks. 

	$ docker service inspect --pretty redis

update the container image

	$ docker service update --image redis:3.0.7 redis
	$ docker service inspect --pretty redis
	$ docker service ps redis

Drain a node on the swarm

	$ docker service create --replicas 3 --name redis --update-delay 10s redis:3.0.6
	$ docker service ps redis
	docker node update --availability drain worker1				## drain a node that had a task assigned to it
	$ docker node inspect --pretty worker1						## Inspect the node to check its availability
	$ docker node update --availability active worker1			## return the drained node to an active state
	$ docker node inspect --pretty worker1
	
# Use swarm mode routing mesh
ref: http://docs.docker-cn.com/engine/swarm/ingress/#publish-a-port-for-tcp-only-or-udp-only  
Publish a port for a service

	$ docker service create \
	  --name <SERVICE-NAME> \
	  --publish <PUBLISHED-PORT>:<TARGET-PORT> \
	  <IMAGE>
    # $ docker service create --name dns-cache -p 53:53/tcp -p 53:53/udp dns-cache      ## Tcp UDP 

You can publish a port for an existing service using the following command:

    $ docker service update \
      --publish-add <PUBLISHED-PORT>:<TARGET-PORT> \
      <SERVICE>

You can use docker service inspect to view the service’s published port. For instance:

    $ docker service inspect --format="{{json .Endpoint.Spec.Ports}}" my-web
    [{"Protocol":"tcp","TargetPort":80,"PublishedPort":8080}]

# Store configuration data using Docker Configs
Docker 17.06 introduces swarm service configs, which allow you to store non-sensitive information, such as configuration files, outside a service’s image or running containers.  
Add a config to Docker

    
    docker@myvm1:~$ echo "This is a config" | docker config create my-config -
    vww0s4bvxxoy81uuvczaddm0e

Create a redis service and grant it access to the config.

    docker@myvm1:~$ docker service  create --name redis --config my-config redis:alpine
    7mr0qhwkronf93epg0wpu3fb5
    overall progress: 1 out of 1 tasks 
    1/1: running   [==================================================>] 
    verify: Service converged 

Verify that the task is running without issues using docker service ps

    docker@myvm1:~$ docker service ps redis
    ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE          ERROR                              PORTS
    v3rhjjwou7dn        redis.1             redis:alpine        myvm1               Running             Running 2 hours ago   

Get the ID of the redis service task container using docker ps

    docker@myvm1:~$ docker ps --filter name=redis -q
    e8eee1795a41
    
use docker exec to connect to the container and read the contents of the config data file

    docker@myvm1:~$ docker exec $(docker ps --filter name=redis -q) ls -l /my-config
    -r--r--r--    1 root     root            17 Apr 26 04:04 /my-config
    docker@myvm1:~$ docker exec $(docker ps --filter name=redis -q) cat /my-config
    This is a config

Try removing the config.

    docker config ls
    docker@myvm1:~$ docker config rm my-config
    Error response from daemon: rpc error: code = InvalidArgument desc = config 'my-config' is in use by the following service: redis

Remove access to the config from the running redis service by updating the service

    docker@myvm1:~$ docker service update --config-rm my-config redis
    redis
    overall progress: 1 out of 1 tasks 
    1/1: running   [==================================================>] 
    verify: Service converged 

    docker@myvm1:~$ docker exec $(docker ps --filter name=redis -q) ls -l /my-config
    ls: /my-config: No such file or directory

Stop and remove the service, and remove the config from Docker

    docker service rm redis
    docker config rm my-config

# Lock your swarm to protect its encryption key
Initialize a swarm with autolocking enabled

    $ docker swarm init --autolock

Enable or disable autolock on an existing swarm

    $ docker swarm update --autolock=true

Unlock a swarm

    $ docker swarm unlock
    Please enter unlock key:

View the current unlock key for a running swarm

    $ docker swarm unlock-key

Rotate the unlock key

    $ docker swarm unlock-key --rotate

