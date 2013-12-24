# Install redmine on Debian-7.3.0

Install mysql & apache

    apt-get install apache2 mysql-server mysql-client -y

Install redmine
    
    apt-get install redmine-mysql -y 
    apt-get install redmine -y 
    apt-get install libapache2-mod-passenger -y
    
All database settings, including the password, are stored here:

    /etc/redmine/default/database.yml
 
Start redmine 

    ln -s /usr/share/redmine/public /var/www/redmine 
    chown -R www-data:www-data /var/www/redmine
    
    vim /etc/apache2/sites-available/redmine
    <VirtualHost *:80>
        DocumentRoot /usr/share/redmine/public/
    
        <Directory "/usr/share/redmine/public/">
                Options Indexes ExecCGI FollowSymLinks
                Order allow,deny
                Allow from all
                AllowOverride all
        </Directory>
    </VirtualHost>

    a2ensite redmine 
    /etc/init.d/apache2 reload
    /etc/init.d/apache2 restart 
    
Configure email

    cp /usr/share/redmine/config/configuration.yml.example /etc/redmine/default/configuration.yml 
 
modify configuration.yml setting email 
 
    default:
      email_delivery:
        delivery_method: :async_smtp
        smtp_settings:
          
          address: smtp.sina.com
          port: 25
          domain: example.net
          authentication: :login
          user_name: redmine@sina.com
          password: "redmine"
          enable_starttls_auto: true

modify default sendmail,设置mail_from为:

    mail_from:
        default: redmine@sina.com 
 
Access redmine

    Visit http://yourserverip . Then login as default Redmine user/password are admin/admin 。
    
# Source code Install redmine 
Download lastest redmine

    cd /opt/
    wget http://www.redmine.org/releases/redmine-2.4.2.tar.gz 
    tar zxvf redmine-2.4.2.tar.gz
    
Create an empty database and accompanying user 

    CREATE DATABASE redmine CHARACTER SET utf8; 
    show databases;
    CREATE USER 'redmine'@'localhost' IDENTIFIED BY 'redmine';
    GRANT ALL PRIVILEGES ON redmine.* TO 'redmine'@'localhost';
    flush privileges;
    
Database connection configuration

    cd /opt/redmine-2.4.2/config/
    cp database.yml.example database.yml 

vim database.yml

    production:
      adapter: mysql
      database: redmine
      host: localhost
      username: redmine
      password: "redmine"
      encoding: utf8 

Dependencies installation 

    gem install bundler 
    
Then you can install all the gems required by Redmine using the following command: 

    bundle install --without development test rmagick 

Session store secret generation 

    rake generate_secret_token 

Database schema objects creation  
Create the database structure, by running the following command under the application root directory:

    RAILS_ENV=production rake db:migrate 
    
Database default data set  
Insert default configuration data in database, by running the following command:

    RAILS_ENV=production rake redmine:load_default_data 
    
File system permissions 

    mkdir -p tmp tmp/pdf public/plugins
    chmod -R 755 files log tmp public/plugins 
    
Test the installation

    ruby script/rails server webrick -e production
 
Logging into the application  
Use default administrator account to log in:

    login: admin
    password: admin

