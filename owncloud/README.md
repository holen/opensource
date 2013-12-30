# Owncloud
## resume
cloud storage for files, music, contacts, calendars and many more 

## Install server on debian7.0

Get apt source 

    echo 'deb http://download.opensuse.org/repositories/isv:ownCloud:community:nightly/Debian_7.0/ /' >> /etc/apt/sources.list.d/owncloud.list  
    
Add apt key

    wget http://download.opensuse.org/repositories/isv:ownCloud:community:nightly/Debian_7.0/Release.key
    apt-key add - < Release.key
    
Install owncloud server

    apt-get update
    apt-cache search owncloud
    apt-get install owncloud
    
## Install sync client on Ubuntu12.04

Get apt source 

    echo 'deb http://download.opensuse.org/repositories/isv:ownCloud:desktop/xUbuntu_12.04/ /' >> /etc/apt/sources.list.d/owncloud-client.list 
    
Add apt key

    wget http://download.opensuse.org/repositories/isv:ownCloud:desktop/xUbuntu_12.04/Release.key
    apt-key add - < Release.key   
    
Install owncloud client 

    apt-get update
    apt-cache search owncloud
    apt-get install owncloud-client 
    
## Start sync client 
    
    owncloud --logdir /var/log/owncloud/ --logexpire 72 --logflush --confdir /data/owncloud/ &
    
Then 

    Input the web as http://ip/owncloud
    Input user/password and select store folder
    
## Owncloud with ssl connection

[How to Setup OwnCloud Server 5 with SSL Connection](http://ubuntuserverguide.com/2013/04/how-to-setup-owncloud-server-5-with-ssl-connection.html)
    

