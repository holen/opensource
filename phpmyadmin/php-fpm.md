# php-fpm
update

    apt-get update
    apt-get upgrade
    rm -rf /etc/udev/rules.d/70-persistent-net.rules

ip network

    sysctl -w net.ipv4.tcp_tw_reuse=1
    sysctl -w net.ipv4.tcp_keepalive_time=1800
    sysctl -w net.ipv4.tcp_fin_timeout=30
    sysctl -w net.ipv4.tcp_keepalive_intvl=30

install 

    apt-get -y install apache2-mpm-worker
    apt-get -y install libapache2-mod-fastcgi php5-fpm php-apc php5
    apt-get -y install php5-memcached php5-curl php5-gd php5-mysql
    a2enmod actions fastcgi alias
    cp /etc/php5/fpm/pool.d/www.conf /etc/php5/fpm/pool.d/www.conf.orig
    cp /etc/php5/fpm/php.ini /etc/php5/fpm/php.ini.orig

modify conf

    sed -i 's!^listen =!; listen =!' /etc/php5/fpm/pool.d/www.conf
    sed -i 's!^disable_functions =!; disable_functions =!' /etc/php5/fpm/php.ini
    sed -i 's!^memory_limit =!; memory_limit =!' /etc/php5/fpm/php.ini
    sed -i 's!^expose_php =!; expose_php =!' /etc/php5/fpm/php.ini
    sed -i 's!^display_errors =!; display_errors =!' /etc/php5/fpm/php.ini
    sed -i 's!^open_basedir =!; open_basedir =!' /etc/php5/fpm/php.ini
    sed -i 's!^chroot =!; chroot=!' /etc/php5/fpm/php.ini

    echo "listen = /var/run/php-fpm.sock" >> /etc/php5/fpm/pool.d/www.conf
    echo "disable_functions = pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsi❯
    echo "memory_limit = 256M" >> /etc/php5/fpm/php.ini
    echo "expose_php = off" >> /etc/php5/fpm/php.ini                                                                       
    echo "display_errors = off" >> /etc/php5/fpm/php.ini

    echo "open_basedir = /data/apache2/wcn" >> /etc/php5/fpm/php.ini
    echo "chroot = /data/apache2/wcn" >> /etc/php5/fpm/php.ini
    echo "listen = /var/run/php-fpm.sock" >> /etc/php5/fpm/pool.d/www.conf
    echo "disable_functions = pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,execute,passthru,exec,system,chroot,scandir,chgrp,chown,shell_exec,proc_open,proc_get_status,ini_alter,ini_restore,dl,openlog,syslog,readlink,symlink,popepassthru,stream_socket_serve,escapeshellarg,escapeshellcmd,proc_close,popen,show_source,phpinfo" >> /etc/php5/fpm/php.ini
    echo "memory_limit = 256M" >> /etc/php5/fpm/php.ini
    echo "expose_php = off" >> /etc/php5/fpm/php.ini
    echo "display_errors = off" >> /etc/php5/fpm/php.ini
    echo "open_basedir = /data/apache2/wcn" >> /etc/php5/fpm/php.ini
    echo "chroot = /data/apache2/wcn" >> /etc/php5/fpm/php.ini
    echo ‘ulimit -HSn 65536′ >> /etc/rc.local

restart

    service php5-fpm restart
    service apache2 restart

enable mod 

    a2enmod rewrite

test

    ab -n 10000 -c 1000 http://xm.e.cn/t.php
    09,39 *     * * *     root   [ -x /usr/lib/php5/maxlifetime ] && [ -d /var/lib/php5 ] && find /var/lib/php5/ -depth -mindepth 1 -maxdepth 1 -type f -cmin +$(/usr/lib/php5/maxlifetime) -print0 | xargs -n 200 -r -0 rm
    webbench -c 200 -t http://xm.e.cn/

php.ini 

    upload_max_filesize = 80M
    post_max_size = 80M
    max_input_time = 600
    max_execution_time = 600
    date.timezone = Asia/Shanghai
    disable_functions = pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,execute,passthru,exec,system,chroot,scandir,chgrp,chown,shell_exec,proc_open,proc_get_status,ini_alter,ini_restore,dl,openlog,syslog,readlink,symlink,popepassthru,stream_socket_serve,escapeshellarg,escapeshellcmd,proc_close,popen,show_source,phpinfo
    memory_limit = 64m
    expose_php = off
    display_errors = off
    open_basedir = /data/apache2/:/tmp/ #将用户可操作的文件限制在某目录下
    chroot = /data/apache2/ #把指定的网站完完全全限制在一个目录下
