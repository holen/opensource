# Nginx Docker Images

Docker container to install and run nginx 1.14.2 on Centos7.5 .

# Environment variables

Use following environment variables to configure docker container php process manager during container boot up:

    NGINX_VERSION=nginx-1.14.2
    NGINX_PREFIX=/usr/local/webserver/nginx

## nginx 配置文件

/usr/local/webserver/nginx/conf

## nginx sbin 执行文件目录

/usr/local/webserver/nginx/sbin/nginx

# 编译模块

    ./configure \
    --prefix=$NGINX_PREFIX \
    --user=www \
    --group=www \
    --with-stream \
    --with-http_ssl_module \
    --with-http_sub_module \
    --with-http_gzip_static_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-debug \
    --with-openssl=../openssl-1.0.2l \
    --with-pcre=../pcre-8.40 \
    --with-zlib=../zlib-1.2.11 \
    --with-ld-opt=-Wl,-rpath,../LuaJIT-2.1.0-beta3/lib \
    --add-module=../ngx_devel_kit-0.3.0 \
    --add-module=../lua-nginx-module-0.10.13 \
    --add-module=../nginx-module-vts

# Pull latest image

    docker login
    docker pull qianbitou/nginx-1.14.2:1.2

# Running as server 

    docker run -d -v $(pwd)/conf/nginx.conf:/usr/local/webserver/nginx/conf/nginx.conf -v $(pwd)/conf/vhosts:/usr/local/webserver/nginx/conf/vhosts qianbitou/nginx-1.14.2:1.2
    docker run -d -v $(pwd)/conf:/usr/local/webserver/nginx/conf qianbitou/nginx-1.14.2:1.2

# Release 

    1.0 nginx 80
    1.1 nginx 80 443
    1.2 nginx 80 443 and add default index
