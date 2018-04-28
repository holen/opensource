# Manage sensitive data with Docker secrets
ref: http://docs.docker-cn.com/engine/swarm/secrets/  

You can use secrets to manage any sensitive data which a container needs at runtime but you don’t want to store in the image or in source control, such as:

    Usernames and passwords
    TLS certificates and keys
    SSH keys
    Other important data such as the name of a database or internal server
    Generic strings or binary content (up to 500 kb in size)

Simple example: Get started with secrets  
Add a secret to Docker
        
        $ echo "This is a secret" | docker secret create my_secret_data -

Create a redis service and grant it access to the secret

        $ docker service  create --name redis --secret my_secret_data redis:alpine

Verify that the task is running without issues using docker service ps

        $ docker service ps redis

Get the ID of the redis service task container using docker ps 

        $ docker ps --filter name=redis -q
        $ docker exec $(docker ps --filter name=redis -q) ls -l /run/secrets
        $ docker exec $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

Verify that the secret is not available if you commit the container

        $ docker commit $(docker ps --filter name=redis -q) committed_redis
        $ docker run --rm -it committed_redis cat /run/secrets/my_secret_data
        cat: can't open '/run/secrets/my_secret_data': No such file or directory

Try removing the secret.

    $ docker secret ls
    $ docker secret rm my_secret_data
    Error response from daemon: rpc error: code = 3 desc = secret
    'my_secret_data' is in use by the following service: redis

Remove access to the secret from the running redis service by updating the service

    $ docker service update --secret-rm my_secret_data redis
    $ docker exec -it $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

Stop and remove the service, and remove the secret from Docker.

    $ docker service rm redis
    $ docker secret rm my_secret_data

Use Secrets in Compose

version: '3.1'

services:
   db:
     image: mysql:latest
     volumes:
       - db_data:/var/lib/mysql
     environment:
       MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_root_password
       - db_password

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_password

secrets:
   db_password:
     file: db_password.txt
   db_root_password:
     file: db_root_password.txt

volumes:
    db_data:



