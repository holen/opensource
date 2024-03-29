# ngins virtual-host server_name 
在一个nginx虚拟机中，可以绑定多个`server_name`, eg:

    server {
       listen       80;
        server_name  www.abc.cn blog.abc.cn *.abc.cn;

*  而`server_name`的先后顺序的不同，对PHP程序中使用`$_SERVER["SERVER_NAME"]`或`getenv('SERVER_NAME')`获取服务器域名是有影响的
*  `$_SERVER["SERVER_NAME"]`或`getenv('SERVER_NAME')`获取的始终将是Nginx `server_name`配置中的第一个域名，这一点在程序开发中需要注意。这第一个域名就相当于Apache虚拟主机配置中的`ServerName`，后面的域名就相当于`Apache的ServerAlias`。

在某些情况下（具体可参考 [wiki.nginx.org](wiki.nginx.org)），Nginx 内部重定向规则会被启动，例如,当 URL 指向一个目录并且在最后没有包含`/`时，Nginx 内部会自动的做一个 301 重定向，这时会有两种情况：

1. `server_name_in_redirect` on（默认），URL 重定向为： server_name 中的第一个域名 + 目录名 + /；
2. `server_name_in_redirect` off，URL 重定向为： 原 URL 中的域名 + 目录名 + /。

当你有多个域名要指向同一个虚拟主机，并且你自己写 301 重定向规则把它们合并到某一个域名时，情况就更复杂了：

1. 首先，nginx 检查 URL，如果符合条件，就用该规则（你写的）做第一遍重定向
2. 接着，检查新生成的 URL，如果符合内部自动重定向之条件，就用前面提到的规则再做一次重定向。

至于 PHP 的 `$_SERVER["SERVER_NAME"]`，在 nginx 中默认是由 nginx 的变量 `$server_name` 提供，这时它和重定向没有关系，始终是 server_name 设置中的第一个域名，但这是可以被改变的，在你的 nginx 配置中找到 fastcgi_param 部分，修改
`fastcgi_param  SERVER_NAME    $server_name;`
为
`fastcgi_param  SERVER_NAME    $host;`
但现在就要注意了，此时的 `$_SERVER["SERVER_NAME"]` 会受你写的和 nginx 自己的重定向规则所影响而变化。

1. 设置 fastcgi_param  SERVER_NAME    $host;
2. 设置 server_name_in_redirect off; 让 nginx 在处理自己内部重定向时不默认使用  server_name 设置中的第一个域名；
3. 不要使用 nginx 的 rewrite 规则来重定向、合并多个域名。

当然，后俩条是完全可选的，前提是你清楚你在做什么并且小心处理这时的`$_SERVER["SERVER_NAME"]`，也许更好的做法是保持 `fastcgi_param  SERVER_NAME    $server_name;` ，然后合理使用 `$_SERVER["SERVER_NAME"]` 和 `$_SERVER["HTTP_HOST"]`。

# use IP access web
    server {
            listen       80 default;
            server_name  10.0.0.103;
            access_log   logs/default.access.log;
            error_log    logs/default.error.log;
            
            location / {
                root   /usr/local/nginx/html/front/web;
                index  index.php index.html index.htm;
            }
    
            location ~ \.php$ {
                root   /usr/local/nginx/html/front/web;
                fastcgi_pass   127.0.0.1:9000;
                fastcgi_index  index.php;
                fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
                include        fastcgi_params;
            }
        }
    }

# upgrade code html setting
    server {
        listen       80;
        server_name  app.abc.cn;
        access_log   /var/log/nginx/app.abc.cn.access.log;
        error_log    /var/log/nginx/app.abc.cn.error.log;
        client_max_body_size         20m;
        root  /data/nginx/app.abc.cn/;
        index        index.php index.html;
        location     / {
            if (-f $document_root/maintenance.html) {
                return 503;
            }
        proxy_pass http://appabc;
        }
        location     /images/shengji_bg.jpg {
            root  /data/nginx/app.abc.cn/;
        }
        error_page 503 @maintenance;
        location @maintenance {
            rewrite ^(.*)$ /maintenance.html break;
        }
    }
    
# limit req speed
> nginx.conf  
`limit_req_zone $binary_remote_addr zone=abcpost:10m rate=1r/s;`  
> site-enables/abc.com  

    location ~ ^/(service\.php) {
        limit_req zone=abcpost burst=1;
        proxy_pass http://webabc;
    }

# proxy cache
nginx.conf

    proxy_cache_path /data/nginx/cache/zone levels=1:2 keys_zone=e-w-cn:80m max_size=10000m inactive=600m;

conf

    proxy_cache e-w-cn;

# CDN real client IP 
add this to abc.com conf

    log_format cdnsrcip '$HTTP_CDN_SRC_IP';

add follow to `server`

    access_log /var/log/nginx/abc.com.access.log cdnsrcip

# Apache setting 

    LogFormat  "%{Cdn-Src-Ip}i %a %A %l %u  %t %V \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\" " cdnsrcip
    CustomLog ${APACHE_LOG_DIR}/access.log cdnsrcip 

    %a - Remote IP address
    %A - Local IP address
    %b - Bytes sent, excluding HTTP headers, or '-' if no bytes were sent
    %B - Bytes sent, excluding HTTP headers
    %h - Remote host name
    %H - Request protocol
    %l - Remote logical username from identd (always returns '-')
    %m - Request method
    %p - Local port
    %q - Query string (prepended with a '?' if it exists, otherwise an empty string
    %r - First line of the request
    %s - HTTP status code of the response
    %S - User session ID
    %t - Date and time, in Common Log Format format
    %u - Remote user that was authenticated
    %U - Requested URL path
    %v - Local server name
    %D - Time taken to process the request, in millis
    %T - Time taken to process the request, in seconds
    %I - current Request thread name (can compare later with stacktraces) 
