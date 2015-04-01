# Install php5-fpm apache on ubuntu
set ulimit 

    ulimit -SHn 65535

    vim /etc/security/limits.conf
    *        soft    noproc  65535
    *        hard    noproc  65535
    *        soft    nofile  65535
    *        hard    nofile  65535
    root        soft    noproc  65535
    root        hard    noproc  65535
    root        soft    nofile  65535
    root        hard    nofile  65535

install apache

    apt-get install apache2-mpm-worker libapache2-mod-fastcgi 

install php5 php5-fpm

    apt-get install php5-fpm php5 php5-gd php5-curl libapache2-mod-auth-mysql php5-mysql mysql-client php5-memcached php5-imagick php5-cli php5-dev 

install apc 

    apt-get install make php-apc
