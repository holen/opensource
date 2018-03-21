# start docker

    docker-compose up -d

# login docker container

    docker exec -it svnserver /bin/bash

# chown docker container dir 

    chown -R www-data.www-data /home/ubuntu/svndata
    chown -R www-data.www-data /etc/apache2/conf
    chown -R www-data.www-data /var/www/html

# sbuversion authorization file

    SVNAuthFile=/etc/apache2/conf/dav_svn.passwd
    SVNUserFile=/etc/apache2/conf/access_svn

# manage docker container

    docker start svnserver
    docker stop svnserver
    docker rm svnserver

