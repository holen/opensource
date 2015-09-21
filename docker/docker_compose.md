# Install docker-compose

    curl -L https://github.com/docker/compose/releases/download/1.4.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    docker-compose --version

# RUN

    docker-compose up -d
    docker ps -a 
    docker-compose stop
    docker-compose ps
    docker-compose rm
    docker-compose ps
