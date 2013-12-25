# install mysql  
$ apt-get install mysql-server libapache2-mod-auth-mysql php5-mysql -y  

# install php  
$ apt-get install php5 libapache2-mod-php5 php5-mcrypt php5-curl -y   

# install phpmyadmin  
apt-get install phpmyadmin -y   

# install php module  
$ apt-get install php5-gd -y  

# test php info  
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
