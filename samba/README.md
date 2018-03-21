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


###############################

useradd -d /data/web/samba -m -s /sbin/nologin qianbitou
pdbedit -a -u qianbitou

[root@linux ~]# testparm
# 这个动作很重要！每次都要进行！确认你的语法无误后再开始！

[root@linux ~]# /etc/init.d/smb restart

[root@linux ~]# smbclient -L //127.0.0.1
Password:                   <==直接按下 [Enter] 即可。
Anonymous login successful  <==是匿名登录喔！
Domain=[VBIRDHOUSE] OS=[Unix] Server=[Samba 3.0.10-1.4E.9]

    Sharename   Type  Comment
    ---------   ----  -------
    public      Disk  the user groups work directory
    temp        Disk  Temporary file space
    IPC$        IPC   IPC Service (This is vbird's samba server)
    ADMIN$      IPC   IPC Service (This is vbird's samba server)

[root@linux ~]# smbclient -L //127.0.0.1 -U dmtsai
Password: <==输入 dmtsai 在 smbpasswd 档案中所建立的密码喔！
Domain=[VBIRDSERVER] OS=[Unix] Server=[Samba 3.0.10-1.4E.9]

    Sharename   Type  Comment
    ---------   ----  -------
    public      Disk  the user groups work directory
    temp        Disk  Temporary file space
    IPC$        IPC   IPC Service (This is vbird's samba server)
    ADMIN$      IPC   IPC Service (This is vbird's samba server)
    dmtsai      Disk  Home directories


pdbedit -L
ll /data/web/
chown -R qiantitou.qianbitou samba
