# Install webvirtmgr
environment

    Ubuntu 14.04 LTS
    python 2.7.6

install some prereq packages including the webserver nginx to host webvirtmgr

    apt-get install git python-pip python-libvirt python-libxml2 novnc supervisor nginx
 
download the git repository

    mkdir /root/git-repos
    cd /root/git-repos
    git clone git://github.com/retspen/webvirtmgr.git
 
configure webvirtmanager

    cd /root/git-repos/webvirtmgr
    sudo pip install -r requirements.txt
 
create database tables (answer yes to create a valid user and specify a username and password of your choice)

    ./manage.py syncdb
    then create a superuser, input username email password

    ./webvirtmgr/manage.py createsuperuser # add another user
 
 
collect static files (answer yes to continue when being asked)

    ./manage.py collectstatic
 
move webvirtmgr to your ngix web directory.

    cd ..
    mv webvirtmgr /var/www/
 
create the file /etc/nginx/sites-available/webvirtmgr.conf and add the following lines

    server {
        listen 80 default_server;
        server_name $hostname;
        #access_log /var/log/nginx/webvirtmgr_access_log; 

        location /static/ {
            root /var/www/webvirtmgr/webvirtmgr; # or /srv instead of /var
            expires max;
        }

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-for $proxy_add_x_forwarded_for;
            proxy_set_header Host $host:$server_port;
            proxy_set_header X-Forwarded-Proto $remote_addr;
            proxy_connect_timeout 600;
            proxy_read_timeout 600;
            proxy_send_timeout 600;
        }
    }
 
activate the webvirtmgr configuration for nginx and remove the default one

    rm /etc/nginx/sites-enabled/default
    ln -sf /etc/nginx/sites-available/webvirtmgr.conf /etc/nginx/sites-enabled/webvirtmgr.conf
 
restart the nginx service

    service nginx restart
 
run the following commands

    service novnc stop
    update-rc.d -f novnc remove
    rm /etc/init.d/novnc
    cp /var/www/webvirtmgr/conf/initd/webvirtmgr-novnc-ubuntu /etc/init.d/webvirtmgr-novnc
    service webvirtmgr-novnc start
    update-rc.d webvirtmgr-novnc defaults
    service webvirtmgr-novnc start
    chown -R www-data:www-data /var/www/webvirtmgr
 
create the file /etc/supervisor/conf.d/webvirtmgr.conf and add the following lines

    [program:webvirtmgr]
    command=/usr/bin/python /var/www/webvirtmgr/manage.py run_gunicorn -c /var/www/webvirtmgr/conf/gunicorn.conf.py
    directory=/var/www/webvirtmgr
    autostart=true
    autorestart=true
    stdout_logfile=/var/log/supervisor/webvirtmgr.log
    redirect_stderr=true
    user=www-data
 
restart the supervisor daemon

    service supervisor restart
 
try logging in to webvirtmgr with the username you've provided in the previous steps
 
    http://192.168.1.30
 
run the following commands to upgrade webvirtmgr in the future

    cd /var/www/webvirtmgr
    git pull
    service supervisor restart
    service webvirtmgr-novnc restart

# Setting up the server to work with the service
Install packages libvirt-bin, KVM, sasl2-bin

    apt-get install kvm libvirt-bin sasl2-bin

Add the option -l in the file /etc/default/libvirt-bin

    libvirtd_opts="-d -l"

The file /etc/libvirt/libvirtd.conf uncomment the line

    listen_tls = 0
    listen_tcp = 1

Restart the daemon libvirtd, because after installation it runs automatically

    service libvirt-bin restart

Adding users and setting their passwords is done with the saslpasswd2 command. When running this command it is important to tell it that the appname is libvirt. As an example, to add a user fred, run

    saslpasswd2 -a libvirt fred
    Password: xxxxxx
    Again (for verification): xxxxxx

To see a list of all accounts the sasldblistusers2 command can be used. This command expects to be given the path to the libvirt user database, which is kept in /etc/libvirt/passwd.db

    $ sudo sasldblistusers2 -f /etc/libvirt/passwd.db
    fred@webvirtmgr.net: userPassword
    To disable a user's access, use the command saslpasswd2 with the -d
    saslpasswd2 -a libvirt -d fred

Test connection

    virsh -c qemu+tcp://IP_address/system nodeinfo
    Please enter your authentication name: fred
    Please enter your password: xxxxxx
    CPU model:           x86_64
    CPU(s):              2
    CPU frequency:       2611 MHz
    CPU socket(s):       1
    Core(s) per socket:  2
    Thread(s) per core:  1
    NUMA cell(s):        1
    Memory size:         2019260 kB


