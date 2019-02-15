# PHP-FPM Docker Images

Docker container to install and run PHP-FPM on Centos7.5 .

# What is PHP-FPM ?

PHP-FPM (FastCGI Process Manager) is an alternative FastCGI implementation for PHP.

# Environment variables

Use following environment variables to configure docker container php process manager during container boot up:

## system user

    PHP_UID=302  
    PHP_GID=302   
    PHP_HOME=/usr/local/webserver/php-70  
    PHP_USER=php  

will run create a system user called php-fpm with UID:GUID 1000:1000 and home directory /app, which then can be referenced in your php-fpm manager pool configuration file.

## php.ini configuration

PHP_INI_PATH=/path/to/php.ini

will include specified php.ini configuration during php-fpm manager start. It allows to use a wildcard in case you would like to include several .ini configuration files.

## php-fpm pool configurations

PHP_POOL_PATH=/path/to/php-fpm.d/www.conf

will include specified pool.conf configuration during php-fpm manager start. It allows to use a wildcard in case you would like to include several .conf configuration files. ATTENTION: default www.conf pool configuration will be loaded, unless you specify path to your custom www.conf.

# Installed extensions

    bcmath
    Core
    ctype
    curl
    date
    dom
    exif
    fileinfo
    filter
    ftp
    gd
    gettext
    hash
    iconv
    json
    ldap
    libxml
    mbstring
    mcrypt
    mysqli
    mysqlnd
    openssl
    pcntl
    pcre
    PDO
    pdo_mysql
    pdo_sqlite
    Phar
    posix
    Reflection
    session
    shmop
    SimpleXML
    soap
    sockets
    SPL
    sqlite3
    standard
    sysvsem
    tokenizer
    xml
    xmlreader
    xmlrpc
    xmlwriter
    Zend OPcache
    zip
    zlib

# Installed Zend Modules

    Zend OPcache

# Pull latest image

    docker login
    docker pull qianbitou/php70-fpm:tagname

# Running as server 

    docker run -d qianbitou/php70-fpm:1.2

# Release 

    1.1		
    1.2		mysql client => 5.6
