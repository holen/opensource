# install mysql  
    
    apt-get install mysql-server libapache2-mod-auth-mysql php5-mysql -y  

# install php  
    
    apt-get install php5 libapache2-mod-php5 php5-mcrypt -y   

# install phpmyadmin  
    
    apt-get install phpmyadmin -y   

# install php module  
    
    apt-get install curl make unzip php5-gd php5-curl php-pear -y  

# install php memcache module
Install memcached

    apt-get install memcached

Install php memcache module

    apt-get install php5-memcached

Test

    php -r "new Memcache();"

# install php redis module
Install redis 

    apt-get install redis-Server

Install php redis module

    wget https://github.com/nicolasff/phpredis/archive/master.zip
    unzip master.zip
    cd phpredis-master
    phpize
    ./configure
    make 
    make install

Configure 

    vim /etc/php5/cli/php.ini
    extension=redis.so
    vim /etc/php5/apache2/php.ini
    extension=redis.so

Test
    
    php -r "phpinfo();" | grep mem
    vim 1
    <?php
    $redis = new Redis();
    $redis->connect('127.0.0.1',6379);
    $redis->set('test','hello world!\n');
    echo $redis->get('test');
    ?>
    # run
    php 1

# install php mongo module
Install mongo

    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
    apt-get update
    apt-cache search mongodb
    apt-get install mongodb-10gen

Install php5-mongo

    wget https://github.com/mongodb/mongo-php-driver/archive/master.zip
    cd mongo-php-driver-master/
    phpize
    ./configure 
    make install

Configure

    vim /etc/php5/cli/php.ini
    extension=mongo.so
    vim /etc/php5/apache2/php.ini
    extension=mongo.so

Test

    vim test
    <?php
    // connect
    $m = new MongoClient();
    // select a database
    $db = $m->comedy;
    // select a collection (analogous to a relational database's table)
    $collection = $db->cartoons;
    // add a record
    $document = array( "title" => "Calvin and Hobbes", "author" => "Bill Watterson" );
    $collection->insert($document);
    // add another record, with a different "shape"
    $document = array( "title" => "XKCD", "online" => true );
    $collection->insert($document);
    // find everything in the collection
    $cursor = $collection->find();
    // iterate through the results
    foreach ($cursor as $document) {
            echo $document["title"] . "\n";
    }
    ?>
    # run 
    php test

# test php info  
Command

     php -r "phpinfo();" | grep memcache
     php -r "phpinfo();" | grep mongo
     php -i | grep extension

$ php --version  
PHP 5.4.4-14+deb7u5 (cli) (built: Oct  3 2013 09:24:58)   
Copyright (c) 1997-2012 The PHP Group  
Zend Engine v2.4.0, Copyright (c) 1998-2012 Zend Technologies  

vim /var/www/info.php  
<?php  
phpinfo();  
?>  

    vim /etc/apache2/sites-available/test.com
    <VirtualHost *:80>
      ServerAdmin webmaster@localhost

      DocumentRoot /var/www/test.com/
      ServerName test.com
      ServerAlias *.test.com
      <Directory />
          Options FollowSymLinks
          AllowOverride All
      </Directory>

      ErrorLog ${APACHE_LOG_DIR}/error.log

      # Possible values include: debug, info, notice, warn, error, crit,
      # alert, emerg.
      LogLevel warn

      CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>

    chown -R  www-data.www-data /var/www/test.com
    a2ensite www.test.com
    service apache2 reload
    a2enmod rewrite
    service apache2 restart

# install ZendOptimizer  
Download ZendGuardLoader-70429-PHP-5.4-linux-glibc23-x86_64.tar.gz  
tar zxvf ZendGuardLoader-70429-PHP-5.4-linux-glibc23-x86_64.tar.gz  
mkdir /usr/local/zend  
cp ZendGuardLoader-70429-PHP-5.4-linux-glibc23-x86_64/php-5.4.x/ZendGuardLoader.so /usr/local/zend/  
vim /etc/php5/apache2/php.ini  
zend_extension="/usr/local/zend/ZendGuardLoader.so"  
/etc/init.d/apache2 restart  

access http://ip/info.php  
Zend Guard Loader	enable  
