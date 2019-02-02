FROM centos:7.5.1804

ENV NGINX_VERSION nginx-1.14.2
ENV NGINX_PREFIX /usr/local/webserver/nginx
ENV PATH="$NGINX_PREFIX/sbin:${PATH}"

RUN id -g www || groupadd www -g 302 && \
    id -u www || useradd -u 302 -g www -c "Web Server" www -s /sbin/nologin -M && \
    cp -rf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN yum -y install pcre-devel  zlib-devel openssl \
    openssl-devel libtool libtool-ltdl lua-devel git lua-devel gcc gcc-c++

ADD http://nginx.org/download/nginx-1.14.2.tar.gz /opt/
ADD https://www.openssl.org/source/openssl-1.0.2l.tar.gz /opt/
ADD https://sourceforge.net/projects/pcre/files/pcre/8.40/pcre-8.40.tar.gz/download /opt/
ADD http://www.zlib.net/zlib-1.2.11.tar.gz /opt/
ADD http://luajit.org/download/LuaJIT-2.1.0-beta3.tar.gz /opt/
ADD https://github.com/simpl/ngx_devel_kit/archive/v0.3.0.tar.gz  /opt/
ADD https://codeload.github.com/openresty/lua-nginx-module/tar.gz/v0.10.13 /opt/

RUN cd /opt/ && \
    tar zxvf nginx-1.14.2.tar.gz && \
    tar zxvf openssl-1.0.2l.tar.gz && \
    tar zxvf download && \
    tar zxvf zlib-1.2.11.tar.gz && \
    tar zxvf LuaJIT-2.1.0-beta3.tar.gz && \
    tar zxvf v0.3.0.tar.gz && \
    tar zxvf v0.10.13 && \
    rm -rf nginx-1.14.2.tar.gz openssl-1.0.2l.tar.gz download zlib-1.2.11.tar.gz LuaJIT-2.1.0-beta3.tar.gz v0.3.0.tar.gz v0.10.13

RUN set -uxe && \
    cd /opt/ && \
    git clone git://github.com/vozlt/nginx-module-vts.git /opt/nginx-module-vts && \
    echo "alias cdn='cd $NGINX_PREFIX'" >> /root/.bashrc && \
    cd /opt/$NGINX_VERSION && \
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
    --add-module=../nginx-module-vts \
    && make \
    && make install \
    && [ ! -d /data/logs ] && mkdir -p /data/logs \
    && mkdir -p /$NGINX_PREFIX/conf/vhosts \
    && rm -rf /opt/* \
    && yum clean all

COPY conf/www.conf $NGINX_PREFIX/conf/vhosts/
COPY conf/cache_set.conf $NGINX_PREFIX/conf/
COPY conf/nginx.conf $NGINX_PREFIX/conf/
COPY conf/php.conf $NGINX_PREFIX/conf/

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
