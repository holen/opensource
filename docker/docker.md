Get the latest Docker package

    wget -qO- https://get.docker.com/ | sh

Find & run the whalesay image

    docker run docker/whalesay cowsay boo
    docker images

Build your own image

    create a Dockerfile
    docker build -t docker-whale . 

Tag & push your image

    docker login --username=user --password=pass --email=abc@qq.com
    docker push holen/docker-whale
    docker pull holen/docker-whale

Hello world
    
    docker run ubuntu:14.04 /bin/echo 'Hello world'

An interactive container

    docker run -t -i ubuntu:14.04 /bin/bash

Run a daemonized Hello world

    docker run -d ubuntu:14.04 /bin/bash -c "while true; do echo hello world; sleep 1; done"
    docker ps
    docker logs cranky_raman
    docker stop cranky_raman

Run a web application container

    docker run -d -P training/webapp python app.py
    docker ps -l
    docker run -d -p 80:5000 training/webapp python app.py
    docker port dreamy_feynman 5000
    docker logs -f dreamy_feynman
    docker top dreamy_feynman
    docker inspect dreamy_feynman
    docker inspect -f '{{ .NetworkSettings.IPAddress }}' dreamy_feynman
    docker stop dreamy_feynman
    docker rm dreamy_feynman

    docker commit -m "Added json gem" -a "Kate Smith" 0b2616b0e5a8 ouruser/sinatra:v2

Remove an image from the host

    docker rmi training/sinatra

Linking containers together

    docker run -d --name db training/postgres
    docker run -d -P --name web --link db:db training/webapp python app.py
    docker inspect -f "{{ .HostConfig.Links }}" web

Managing data in containers

    docker run -d -P --name web -v /webapp training/webapp python app.py
    docker inspect web
    docker run -d -P --name web -v /src/webapp:/webapp:ro training/webapp python app.py
    docker run --rm -it -v ~/.bash_history:/.bash_history ubuntu /bin/bash

Creating and mounting a data volume container

    docker create -v /dbdata --name dbdata training/postgres /bin/true
    docker run -d --volumes-from dbdata --name db1 training/postgres
    docker run -d --volumes-from dbdata --name db2 training/postgres
    docker rm -v dbdata

Backup, restore, or migrate data volumes 

    backup:
    docker run --volumes-from dbdata -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
    restore:
    docker run -v /dbdata --name dbdata2 ubuntu /bin/bash
    docker run --volumes-from dbdata2 -v $(pwd):/backup ubuntu cd /dbdata && tar xvf /backup/backup.tar

Get started with Docker Hub

    docker login
    docker search centos
    docker pull centos
    docker push yourname/newimage
    
# git clone https://git.oschina.net/dockerf/docker-training.git
