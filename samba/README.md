# Install samba on ubuntu12.04

install samba

    apt-get install samba

set conf

    [global]
    workgroup = WORKGROUP
    display charset = UTF-8
    unix charset = UTF-8
    dos charset = cp936
    server string = %h server (Samba, Ubuntu)
    dns proxy = no
    log file = /var/log/samba/log.%m
    max log size = 1000
    syslog = 0
    panic action = /usr/share/samba/panic-action %d
    security = user
    username map = /etc/samba/smbusers
    encrypt passwords = true
    passdb backend = tdbsam
    obey pam restrictions = yes
    unix password sync = yes
    passwd program = /usr/bin/passwd %u
    passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .
    pam password change = yes
    map to guest = bad user
    usershare allow guests = yes

    [static]
    comment = static 
    valid users = tomcat6
    path = /data/tomcat6/diy/static
    public = yes
    writable = yes
    create mask = 0755
    directory mask = 0755
    available = yes
    browseable = yes 
    [views]
    comment = views 
    valid users = tomcat6
    path = /data/tomcat6/diy/WEB-INF/views
    public = yes
    writable = yes
    create mask = 0755
    directory mask = 0755
    available = yes
    browseable = yes 

edit /etc/samba/smbusers

    cat /etc/samba/smbusers 
        tomcat6 = tomcat6

set passwd for user

    useradd tomcat6
    smbpasswd -a tomcat6
    smbpasswd -x tomcat6 -- delete 
