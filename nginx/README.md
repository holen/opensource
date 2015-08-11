# nginx configure

 wget --user-agent='windows' http://xm.e.cn/city.html

cache:

    open_log_cache
    open_file_cache
    fastcgi_cache
    proxy_cache

读写分离
    
location / {
    proxy_pass http://web-read/;
    if ($request_method = "PUT") {
        proxy_pass http://web-write;
    }
}

wiki.nginx.org
