# Ubuntu 12.04安装配置Postfix dovecot cyrus sasl(mysql虚拟用户)

本文是基于Ubuntu 12.04配置的邮件服务器，利用postfix提供邮件smtp服务，dovecot提供pop3或imap代理收信服务。使用mysql管理和验证邮件用户。以下操作经本人亲试通过，涉及域名CentOS.bz的请替换为自己的。

一、安装必要包

    apt-get install postfix postfix-mysql postfix-doc mysql-client mysql-server dovecot-common dovecot-imapd dovecot-pop3d libsasl2-2 libsasl2-modules libsasl2-modules-sql sasl2-bin libpam-mysql openssl telnet mailutils dovecot-mysql

二、设置MySQL数据库

    mysql -u root -p
    mysql> CREATE DATABASE mail;
    mysql> USE mail;
    mysql> GRANT SELECT, INSERT, UPDATE, DELETE ON mail.* TO 'mail_admin'@'localhost' IDENTIFIED BY 'password-for-mail_admin';
    mysql> GRANT SELECT, INSERT, UPDATE, DELETE ON mail.* TO 'mail_admin'@'127.0.0.1' IDENTIFIED BY 'password-for-mail_admin';
    mysql> FLUSH PRIVILEGES;
    mysql> CREATE TABLE domains (domain varchar(50) NOT NULL, PRIMARY KEY (domain) );
    mysql> CREATE TABLE forwardings (source varchar(80) NOT NULL, destination TEXT NOT NULL, PRIMARY KEY (source) );
    mysql> CREATE TABLE users (email varchar(80) NOT NULL, password varchar(20) NOT NULL, PRIMARY KEY (email) );
    mysql> CREATE TABLE transport ( domain varchar(128) NOT NULL default '', transport varchar(128) NOT NULL default '', UNIQUE KEY domain (domain) );
    mysql> quit

    注：请替换password-for-mail_admin为用户mail_admin的密码，以下出现password-for-mail_admin的也请替换下。

三、配置Postfix使用MySQL

文件：/etc/postfix/mysql-virtual_domains.cf

    user = mail_admin
    password = password-for-mail_admin
    dbname = mail
    query = SELECT domain as virtual FROM domains WHERE domain='%s'
    hosts = 127.0.0.1

文件：/etc/postfix/mysql-virtual_forwardings.cf

    user = mail_admin
    password = password-for-mail_admin
    dbname = mail
    query = SELECT destination FROM forwardings WHERE source='%s'
    hosts = 127.0.0.1

文件：/etc/postfix/mysql-virtual_mailboxes.cf

    user = mail_admin
    password = password-for-mail_admin
    dbname = mail
    query = SELECT CONCAT(SUBSTRING_INDEX(email,'@',-1),'/',SUBSTRING_INDEX(email,'@',1),'/') FROM users WHERE email='%s'
    hosts = 127.0.0.1

文件：/etc/postfix/mysql-virtual_email2email.cf

    user = mail_admin
    password = password-for-mail_admin
    dbname = mail
    query = SELECT email FROM users WHERE email='%s'
    hosts = 127.0.0.1

设置权限：

    chmod o= /etc/postfix/mysql-virtual_*.cf
    chgrp postfix /etc/postfix/mysql-virtual_*.cf

建立用户：

    groupadd -g 5000 vmail
    useradd -g vmail -u 5000 vmail -d /home/vmail -m

配置postfix:

    postconf -e 'myhostname = shuame.org'
    postconf -e 'mydestination = shuame.org, localhost, localhost.localdomain'
    postconf -e 'mynetworks = 127.0.0.0/8'
    postconf -e 'message_size_limit = 30720000'
    postconf -e 'virtual_alias_domains ='
    postconf -e 'virtual_alias_maps = proxy:mysql:/etc/postfix/mysql-virtual_forwardings.cf, mysql:/etc/postfix/mysql-virtual_email2email.cf'
    postconf -e 'virtual_mailbox_domains = proxy:mysql:/etc/postfix/mysql-virtual_domains.cf'
    postconf -e 'virtual_mailbox_maps = proxy:mysql:/etc/postfix/mysql-virtual_mailboxes.cf'
    postconf -e 'virtual_mailbox_base = /home/vmail'
    postconf -e 'virtual_uid_maps = static:5000'
    postconf -e 'virtual_gid_maps = static:5000'
    postconf -e 'smtpd_sasl_auth_enable = yes'
    postconf -e 'broken_sasl_auth_clients = yes'
    postconf -e 'smtpd_sasl_authenticated_header = yes'
    postconf -e 'smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination'
    postconf -e 'smtpd_use_tls = yes'
    postconf -e 'smtpd_tls_cert_file = /etc/postfix/smtpd.cert'
    postconf -e 'smtpd_tls_key_file = /etc/postfix/smtpd.key'
    postconf -e 'proxy_read_maps = $local_recipient_maps $mydestination $virtual_alias_maps $virtual_alias_domains $virtual_mailbox_maps $virtual_mailbox_domains $relay_recipient_maps $relay_domains $canonical_maps $sender_canonical_maps $recipient_canonical_maps $relocated_maps $transport_maps $mynetworks $virtual_mailbox_limit_maps'
    postconf -e 'virtual_transport = dovecot'
    postconf -e 'local_transport = dovecot'

四、为postfix创建证书：

    cd /etc/postfix
    openssl req -new -outform PEM -out smtpd.cert -newkey rsa:2048 -nodes -keyout smtpd.key -keyform PEM -days 365 -x509

更改证书权限：

    chmod o= /etc/postfix/smtpd.key

五、配置saslauthd

    mkdir -p /var/spool/postfix/var/run/saslauthd
    cp -a /etc/default/saslauthd /etc/default/saslauthd.bak

编辑文件：/etc/default/saslauthd，按以下内容修改：

    START=yes
    DESC="SASL Authentication Daemon"
    NAME="saslauthd"
    MECHANISMS="pam"
    MECH_OPTIONS=""
    THREADS=5
    OPTIONS="-c -m /var/spool/postfix/var/run/saslauthd -r"

文件：/etc/pam.d/smtp

    auth required pam_mysql.so user=mail_admin passwd=password-for-mail_admin host=127.0.0.1 db=mail table=users usercolumn=email passwdcolumn=password crypt=1
    account sufficient pam_mysql.so user=mail_admin passwd=password-for-mail_admin host=127.0.0.1 db=mail table=users usercolumn=email passwdcolumn=password crypt=1

文件：/etc/postfix/sasl/smtpd.conf

    pwcheck_method: saslauthd
    mech_list: plain login
    allow_plaintext: true
    auxprop_plugin: sql
    sql_engine: mysql
    sql_hostnames: 127.0.0.1
    sql_user: mail_admin
    sql_passwd: password-for-mail_admin
    sql_database: mail
    sql_select: select password from users where email = '%u@%r'

设置权限：

    chmod o= /etc/pam.d/smtp
    chmod o= /etc/postfix/sasl/smtpd.conf

重启服务：

    adduser postfix sasl
    postfix -n
    service postconf restart
    service saslauthd restart

六、配置Dovecot

文件：/etc/postfix/master.cf，按如下修改

取消submission配置的注释：

    submission inet n - - - - smtpd
      -o syslog_name=postfix/submission
      -o smtpd_tls_security_level=encrypt
      -o smtpd_sasl_auth_enable=yes
      -o smtpd_client_restrictions=permit_sasl_authenticated,reject
      -o milter_macro_daemon_name=ORIGINATING

文件尾增加：

    dovecot unix - n n - - pipe
      flags=DRhu user=vmail:vmail argv=/usr/lib/dovecot/deliver -d ${recipient}

    cp -a /etc/dovecot/dovecot.conf /etc/dovecot/dovecot.conf.bak

清空文件/etc/dovecot/dovecot.conf，加入如下：

    log_timestamp = "%Y-%m-%d %H:%M:%S "
    mail_location = maildir:/home/vmail/%d/%n/Maildir
    namespace {
    inbox = yes
    location =
    prefix = INBOX.
    separator = .
    type = private
    }
    passdb {
    args = /etc/dovecot/dovecot-sql.conf
    driver = sql
    }
    protocols = imap pop3
    service auth {
    unix_listener /var/spool/postfix/private/auth {
    group = postfix
    mode = 0660
    user = postfix
    }
    unix_listener auth-master {
    mode = 0600
    user = vmail
    }
    user = root
    }
    ssl = required
    ssl_cert = </etc/ssl/certs/dovecot.pem
    ssl_key = </etc/ssl/private/dovecot.pem
    userdb {
    args = uid=5000 gid=5000 home=/home/vmail/%d/%n allow_all_users=yes
    driver = static
    }
    protocol lda {
    auth_socket_path = /var/run/dovecot/auth-master
    log_path = /home/vmail/dovecot-deliver.log
    postmaster_address = postmaster@example.com
    }
    protocol pop3 {
    pop3_uidl_format = %08Xu%08Xv
    }

cp -a /etc/dovecot/dovecot-sql.conf /etc/dovecot/dovecot-sql.conf.bak

文件：/etc/dovecot/dovecot-sql.conf

    driver = mysql
    connect = host=127.0.0.1 dbname=mail user=mail_admin password=password-for-mail_admin
    default_pass_scheme = CRYPT
    password_query = SELECT email as user, password FROM users WHERE email='%u';
    dovecot -n
    service dovecot restart


    chgrp vmail /etc/dovecot/dovecot.conf
    chmod g+r /etc/dovecot/dovecot.conf

七、设置Mail Aliases

文件/etc/aliases
    postmaster: root
    root: postmaster@centos.bz

八、测试

    mysql -u root -p
    USE mail;
    INSERT INTO domains (domain) VALUES ('centos.bz');
    INSERT INTO users (email, password) VALUES ('sales@centos.bz', ENCRYPT('password-for-sales'));
    quit

这里添加了一个sales@centos.bz的用户，密码为password-for-sales，最后，可以使用邮件客户端，如foxmail进行收信和发信的测试

    postqueue -p


# 参考文献
[postfix](http://www.linuxde.net/2013/06/14209.html)
