# FastDFS 
FastDFS is an open source high performance distributed file system (0 < file size < 500M).   
It's major functions include: file storing, file syncing and file accessing, and design for high capacity and load balancing.   
FastDFS has two roles: tracker and storage.  
The tracker takes charge of scheduling and load balancing for file access.   
The storage store files and it's function is file management including: file storing, file syncing, providing file access interface.   

## Install on ubuntu12.04.3
Install prepare

    apt-get update
    apt-get install -y gcc make libevent-dev -y
    
Install libevent

    wget https://github.com/downloads/libevent/libevent/libevent-2.0.21-stable.tar.gz
    tar zxvf libevent-2.0.21-stable.tar.gz
    cd libevent-2.0.21-stable
    ./configure --prefix=/usr
    make clean
    make
    make install

Download FastDFS

    wget http://fastdfs.googlecode.com/files/FastDFS_v4.06.tar.gz 
    tar zxvf FastDFS_v4.06.tar.gz
    
Make all 
    
    cd FastDFS
    vim make.sh
        if [ -f /usr/lib/libpthread.so ] || [ -f /usr/local/lib/libpthread.so ] || [ -f /lib64/libpthread.so ] || [ -f /usr/lib64/libpthread.so ] || [ -f /usr/lib/x86_64-linux-gnu/libpthread.so ] || [ -f /usr/lib/libpthread.a ] || [ -f /usr/local/lib/libpthread.a ] || [ -f /lib64/libpthread.a ] || [ -f /usr/lib64/libpthread.a ] || [ -f /usr/lib/x86_64-linux-gnu/libpthread.a ]; then 
    
    ./make.sh
    
Make install 

    vim client/fdfs_link_library.sh.in 
      ln -fs $TARGET_LIB/libfastcommon.so.1 /usr/lib/libfastcommon.so
      ln -fs $TARGET_LIB/libfdfsclient.so.1 /usr/lib/libfdfsclient.so
      
    ./make.sh install
    
Install php client 
    
    apt-get install php5 php5-dev php5-cli
    cd php_client
    phpize
    ./configure --with-php-config=/usr/bin/php-config 
    make
    make install
    
Test php client 

    if no /etc/php5/apache2/conf.d/fastdfs_client.ini , run : cp fastdfs_client.ini /etc/php5/apache2/conf.d
    service apache2 restart
    php -r "phpinfo();" | grep fastdfs --> is enable ?
    php fastdfs_test.php
    
vim test.php

    < ?php
    //所上传的文件
    $filename = "aa.php";
    //调用FastDFS类
    $fdfs = new FastDFS();
    //上传文件 $filename 是所上传的文件，html是上传后的更名后缀名为.html
    $file_info = $fdfs->storage_upload_by_filename($filename,html);
    //输出上传文件目录和文件名
    echo $file_info['filename'];
    ?> 
    
`php test.php`
 
Modify conf

`mkdir -p /var/www/fastdfs`  
`mkdir -p /var/www/fastdfs/storage` 

vim /etc/fdfs/tracker.conf
    
    base_path=/var/www/fastdfs 
    http.server_port=8090 
    
vim /etc/fdfs/http.conf 

    http.anti_steal.token_check_fail=/var/www/fastdfs/conf/anti-steal.jpg
    
Start tracker

    /usr/local/bin/fdfs_trackerd /etc/fdfs/tracker.conf 

vim /etc/fdfs/storage.conf

    base_path=/var/www/fastdfs/storage
    store_path0=/var/www/fastdfs/storage
    tracker_server=10.0.0.66:22122 
    tracker_server=10.0.0.58:22122 # 可以绑定多个tracker_server避免单点故障
    
Start storage

    /usr/local/bin/fdfs_storaged /etc/fdfs/storage.conf

vim /etc/fdfs/client

    base_path=/var/www/fastdfs
    tracker_server=10.0.140.66:22122 
    http.tracker_server_port=8090 
    #include http.conf   --> 去掉一个#
    
Upload file

    # test env
    fdfs_test /etc/fdfs/client.conf upload FastDFS_v4.06.tar.gz 
    #fdfs_upload_file 上传后不可以修改，只能先删除再上传 
    #fdfs_test、fdfs_test1是FastDFS自带的测试程序，会对一个文件上传两次，分别作为主文件和从文件。返回的文件ID也是两个。
    # 主文件ID = 主文件名 + 主文件扩展名
    # 从文件ID = 主文件名 + 从文件后缀名 + 从文件扩展名
    fdfs_upload_file /etc/fdfs/client.conf /etc/nginx/nginx.conf 
    # fdfs_append_file 上传后可以修改
    fdfs_append_file <config_filename> <appender_file_id> <local_filename>

View file info

    fdfs_file_info /etc/fdfs/client.conf group1/M00/00/00/CgCMOlMBfwSAafr0AAALklGBQYw16.conf

Download file

     fdfs_download_file /etc/fdfs/client.conf group1/M00/00/00/CgCMOlL9fx6AbuC6AAAVlCq4RtQ5577_big.sh make.sh

Delete files
    
    fdfs_delete_file /etc/fdfs/client.conf group1/M00/00/00/CgCMOlMBfwSAafr0AAALklGBQYw16.conf
    
Run the monitor program:

    /usr/local/bin/fdfs_monitor /etc/fdfs/storage.conf
    
Delete storage server

    /usr/local/bin/fdfs_monitor <config_filename> delete <group_name> <storage_ip>
    eg: /usr/local/bin/fdfs_monitor /etc/fdfs/client.conf delete group1 192.168.0.100
    # storage_server ACTIVE 下是无法删除的

# fastdfs nginx module 
Get fastdfs-nginx-module

    cd /usr/local/
    wget http://fastdfs.googlecode.com/files/fastdfs-nginx-module_v1.15.tar.gz  
    tar zxvf fastdfs-nginx-module_v1.15.tar.gz 

Install nginx

    cd /usr/local/
    wget http://nginx.org/download/nginx-1.5.9.tar.gz 
    tar zxvf nginx-1.5.9.tar.gz 
    cd nginx-1.5.9/ 
    apt-get install libssl-dev zlib1g-dev libpcre3-dev libpcre3 php5-gd libgd2-xpm libgd2-xpm-dev  libgeoip-dev 
    ./configure --sbin-path=/usr/sbin --prefix=/etc/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-client-body-temp-path=/var/lib/nginx/body --http-log-path=/var/log/nginx/access.log --http-proxy-temp-path=/var/lib/nginx/proxy --lock-path=/var/lock/nginx.lock --pid-path=/var/run/nginx.pid --with-debug --with-http_addition_module --with-http_dav_module --with-http_geoip_module --with-http_gzip_static_module --with-http_image_filter_module --with-http_stub_status_module --add-module=/usr/local/fastdfs-nginx-module/src/ 
    make 
    make install
    mkdir -p /var/lib/nginx/body
    cp ../fastdfs-nginx-module/src/mod_fastdfs.conf /etc/fdfs/ 
    
Start nginx

    nginx
    
Stop nginx

    pkill nginx
    
vim /etc/fdfs/mod_fastdfs.conf

    base_path=/var/www/fastdfs 
    tracker_server=10.0.10.66:22122 
    storage_server_port=23000 
    group_name=group1           --> storage conf group
    url_have_group_name = true  --> necessary
    store_path0=/var/www/fastdfs/storage 
    
    [group1]
    group_name=group1
    storage_server_port=23000
    store_path_count=1
    store_path0=/var/www/fastdfs/storage 
    
vim /etc/nginx/nginx.conf 

    server 
        listen       8090; 
        
    location /M00 {
            ngx_fastdfs_module;
    }

    location ~ /group[0-9]/M00 {
         ngx_fastdfs_module;
    }
 
Restart nginx 

Test

    fdfs_test /etc/fdfs/client.conf upload storage.conf 
    root@ubuntu:/etc/fdfs# curl -I http://10.0.10.66:8090/group1/M00/00/00/CgCMOlL9i6iAA-M2AAAdKGs7_DQ14_big.conf
    HTTP/1.1 200 OK
    Server: nginx/1.5.9
    Date: Fri, 14 Feb 2014 03:21:25 GMT
    Content-Length: 7464
    Last-Modified: Fri, 14 Feb 2014 03:21:12 GMT
    Connection: keep-alive
    Accept-Ranges: bytes

# Install python client
Download python-client
    
    wget https://fastdfs.googlecode.com/files/fdfs_client-py-1.2.6.tar.gz
    tar zxvf fdfs_client-py-1.2.6.tar.gz
    cd fdfs_client-py-1.2.6
    apt-get install python-dev
    python setup.py install
 
## FastDFS文件下载恢复原始文件名 
在url后面增加一个参数，指定原始文件名

    http://121.14.161.48:9030/group2/M00/00/89/eQ6h3FKJf_PRl8p4AUz4wO8tqaA688.apk?attname=filename.apk 
    
Modify nginx.conf 

    location ~ /group[0-9]/M00 {
    # root /data/store/data;
    if ($arg_attname ~ "^(.*).apk") {
        add_header Content-Disposition "attachment;filename=$arg_attname";
    }
    ngx_fastdfs_module;
    }   
  
## 参考文献
[FastDFS 官网](https://code.google.com/p/fastdfs/)  
[FastDFS 配置教程](http://blog.irebit.com/fastdfs-配置教程/)   
[分布式文件系统FastDFS部署实践](http://www.zrwm.com/?p=4567)  
[ubuntu+FastDFS php_client 安装 api](http://www.cnblogs.com/yeseason/archive/2012/06/29/2570382.html)  
[分布式文件系统FastDFS原理介绍](http://tech.uc.cn/?p=221)  
[FastDFS使用经验分享](http://tech.uc.cn/?p=2579)
