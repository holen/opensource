# Introduction
    fail2ban可以监视你的系统日志，然后匹配日志的错误信息（正则式匹配）执行相应的屏蔽动作（一般情况下是调用防火墙屏蔽），
    如:当有人在试探你的SSH、SMTP、FTP密码，只要达到你预设的次数，fail2ban就会调用防火墙屏蔽这个IP，而且可以发送e-mail通知系统管理员，是一款很实用、很强大的软件！

    它的主要功能有：
    支持大量服务。如sshd,apache,qmail,proftpd,sasl等等
    支持多种动作。如iptables,tcp-wrapper,shorewall(iptables第三方工具),mail notifications(邮件通知)等等。
    在logpath选项中支持通配符
    需要Gamin支持(注：Gamin是用于监视文件和目录是否更改的服务工具)
    需要安装python,iptables,tcp-wrapper,shorewall,Gamin。如果想要发邮件，那必须安装postfix/sendmail
    client/server和多线程

# Install 
    apt-cache search fail2ban
    apt-get install fail2ban

# Install on centos 6.5

    wget http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    rpm -i epel-release-6-8.noarch.rpm
    yum -y install fail2ban

# Usage
## Definitions
    fail2ban包含下面5个要素，理解这5个要素之间的关系，对于如何配置如何使用fail2ban是很有帮助的

    filter（过滤器）：用于在日志文件中找出需要屏蔽信息的正则表达式
    action（操作指令）：发现需要屏蔽时所做的具体操作
    jail（组合，一个filter或者多个action）：filter和action的整合
    fail2ban-client：与fail2ban-server通讯，可以通过它设置server的config文件参数
    fail2ban-server：监控日志文件和执行action

## Configuration
    fail2ban默认的配置文件路径是/etc/fail2ban. 我们可以用fail2ban-client -c <dir> 重新指定配置文件

    A typical configuration tree looks like this:
    action.d/
    fail2ban.conf
    filter.d/
    jail.conf
    
    可以在jail.conf 里面，设置匹配相应的filter就去触发相应的action，只要在filter.d目录下设置相应的conf，在action.d目录下配置相应的action的conf文件。
    eg:
    jail.conf

    [DEFAULT] # 全局配置
    ignoreip = 127.0.0.1/8 ## 忽略IP，此清单的IP不会被屏蔽
    bantime  = 600 ## 屏蔽时间，以秒为单位
    findtime = 60 ##  #监测时间。在此期间内重试超过规定次数，会激活fail2ban采取相应的动作。
    maxretry = 3 ## 最大重试次数
    backend = auto #日志修改检测机制（gamin、polling和auto这三种）
    destemail = root@localhost
    banaction = iptables ## 默认的屏蔽动作
    mta = sendmail
    protocol = tcp
    chain = INPUT
    action_ = %(banaction)s[name=%(__name__)s, port="%(port)s", protocol="%(protocol)s", chain="%(chain)s"]
    [ssh] ## 子段配置，这会覆盖全局设置的参数
    enabled  = true # 是否激活
    port     = ssh
    filter   = sshd # sshd对应filter.d/sshd.conf文件，在此文件下设置相应的匹配规则
    logpath  = /var/log/auth.log
    maxretry = 2 # 最大重试次数,会覆盖全局配置的maxretry
    banaction = iptables[name=ssh,port=22,protocol=tcp]
                mail[name=SSH,dest=toto@titi.com]
                # dummy对应action.d/dummy.conf文件，在此文件下设置相应的触发动作
    
    filter.d目录主要包含企图破入和密码失败的正则表达式,
    eg:filter.d/sshd-ddos.conf 

    [INCLUDES]
    before = common.conf
    [Definition]
    _daemon = sshd
    failregex = ^%(__prefix_line)s(?:error: PAM: )?Authentication failure for .* from <HOST>\s*$
                ^%(__prefix_line)s(?:error: PAM: )?User not known to the underlying authentication module for .* from <HOST>\s*$
                ^%(__prefix_line)sFailed (?:password|publickey) for .* from <HOST>(?: port \d*)?(?: ssh\d*)?$
                ^%(__prefix_line)sROOT LOGIN REFUSED.* FROM <HOST>\s*$
                ^%(__prefix_line)s[iI](?:llegal|nvalid) user .* from <HOST>\s*$
                ^%(__prefix_line)sUser .+ from <HOST> not allowed because not listed in AllowUsers$
                ^%(__prefix_line)sauthentication failure; logname=\S* uid=\S* euid=\S* tty=\S* ruser=\S* rhost=<HOST>(?:\s+user=.*)?\s*$
                ^%(__prefix_line)srefused connect from \S+ \(<HOST>\)\s*$
                ^%(__prefix_line)sAddress <HOST> .* POSSIBLE BREAK-IN ATTEMPT!*\s*$
                ^%(__prefix_line)sUser .+ from <HOST> not allowed because none of user's groups are listed in AllowGroups\s*$
    gnoreregex =

    eg：
    ^%(__prefix_line)sFailed (?:password|publickey) for .* from <HOST>(?: port \d*)?(?: ssh\d*)?$
    上面的匹配规则将会匹配/var/log/auth.log日志文件的如下一行
    Jan 10 07:02:37 homebrou sshd[18419]: Failed password for root from 222.76.213.151 port 55236 ssh2

    在编辑filter.d配置文件时，需要注意的东西如下：
    匹配到的主机名和IP都要用<>包起来，eg:<host>
    In the action scripts, the tag <ip> will be replaced by the IP address of the host that was matched in the <host> tag. 
    可以使用fail2ban-regex来验证规则：
    fail2ban-regex 'Jul 18 12:13:01 [1.2.3.4] authentication failed'     '\[<HOST>\] authentication failed'
    
    action.d目录包含不同的action脚本

    fail2ban-client -d  ## will dump the current configuration. 
    test a single regular expression failregex with a single line of your logfile,eg:
    fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf
    
    cat action.d/iptables-multiport.conf | grep -v ^# | grep -v ^$

    [Definition]
    actionstart = iptables -N fail2ban-<name>
                  iptables -A fail2ban-<name> -j RETURN
                  iptables -I <chain> -p <protocol> -m multiport --dports <port> -j fail2ban-<name>
    actionstop = iptables -D <chain> -p <protocol> -m multiport --dports <port> -j fail2ban-<name>
                 iptables -F fail2ban-<name>
                 iptables -X fail2ban-<name>
    actioncheck = iptables -n -L <chain> | grep -q fail2ban-<name>
    actionban = iptables -I fail2ban-<name> 1 -s <ip> -j DROP
    actionunban = iptables -D fail2ban-<name> -s <ip> -j DROP
    [Init]
    name = default
    port = ssh
    protocol = tcp
    chain = INPUT

# Command

    $ fail2ban-client -d # We will first test whether the configuration directory can be parse correctly. 
    $ fail2ban-client set loglevel 3
    $ fail2ban-client status 
    $ fail2ban-client status ssh
    $ fail2ban-client -h 
    $ fail2ban-client reload
    
# Test
    设置jail.conf的ssh服务如下，把banaction指向dummy，dummy是应用action.d/dummy.conf文件，它会记录3次登录失败的IP到/tmp/fail2ban.dummy中。

    [ssh]
    enabled  = true
    port     = ssh
    filter   = sshd
    logpath  = /var/log/auth.log
    maxretry = 3
    banaction = dummy
   
    $ ssh ip # 重复运行三次错误的密码  

    $ cat /tmp/fail2ban.dummy 
    123
    +10.0.10.101
