FROM centos:7.5.1804

ENV PHP_FPM_USER php
ENV PHP_FPM_GROUP php
ENV PHP_VERSION php-7.0.26
ENV PHP_PREFIX /usr/local/webserver/php-70
ENV PATH="$PHP_PREFIX/bin:$PHP_PREFIX/sbin:${PATH}"

RUN id -g $PHP_FPM_GROUP || groupadd $PHP_FPM_GROUP -g 303 && \
    id -u $PHP_FPM_USER || useradd -u 303 -g $PHP_FPM_GROUP -c "Web Server" $PHP_FPM_USER -s /sbin/nologin -M && \
    id -g www || groupadd www -g 302 && \
    id -u www || useradd -u 302 -g www -c "Web Server" www -s /sbin/nologin -M && \
    cp -rf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN yum install -y epel-release && \ 
    yum install -y gcc zlib-devel \
    libxml2-devel libjpeg-devel libpng-devel \
    freetype-devel curl curl-devel bzip2 bzip2-devel \
    openldap openldap-devel patch libxml2-devel mysql mysql-devel \
    libtiff-devel fontconfig-devel libXpm-devel gettext-devel \
    pam-devel libidn libidn-devel openssl openssl-devel mhash \ 
    mhash-devel mcrypt libmcrypt libmcrypt-devel libssh2 libssh2-devel

ADD $PHP_VERSION.tar.gz /opt/

RUN set -uxe && \
    echo "alias cdp='cd $PHP_PREFIX'" >> /root/.bashrc && \
    cd /opt/$PHP_VERSION && \
    ./configure \
    --prefix=$PHP_PREFIX \
    --with-config-file-path=$PHP_PREFIX/etc \
    --with-libdir=lib64 \
    --with-mysqli=mysqlnd \
    --with-pdo-mysql=mysqlnd \
    --with-pdo-sqlite \
    --with-iconv \
    --with-freetype-dir \
    --with-jpeg-dir \
    --with-png-dir \
    --with-gd \
    --with-zlib \
    --with-libxml-dir \
    --with-curl \
    --with-openssl \
    --with-mhash \
    --with-xmlrpc \
    --with-mcrypt \
    --with-ldap \
    --with-ldap-sasl \
    --with-gettext \
    --enable-fpm \
    --enable-xml \
    --enable-bcmath \
    --enable-shmop \
    --enable-sysvsem \
    --enable-inline-optimization \
    --enable-mbregex \
    --enable-mbstring \
    --enable-exif \
    --enable-gd-native-ttf \
    --enable-pcntl \
    --enable-sockets \
    --enable-zip \
    --enable-soap \
    --enable-pdo \
    --enable-opcache \
    --enable-mysqlnd \
    --disable-debug \
    --disable-ipv6 \
    --disable-rpath \
    && make -j2 \ 
    && make install \
    && cp ./sapi/fpm/init.d.php-fpm $PHP_PREFIX/sbin/ \
    && chmod +x $PHP_PREFIX/sbin/init.d.php-fpm \
    && [ ! -d $PHP_PREFIX/log ] && mkdir -p $PHP_PREFIX/log \
    && rm -rf /opt/$PHP_VERSION \
    && yum clean all

COPY conf/php.ini $PHP_PREFIX/etc/php.ini
COPY conf/php-fpm.conf $PHP_PREFIX/etc/php-fpm.conf
COPY conf/www.conf $PHP_PREFIX/etc/php-fpm.d/

EXPOSE 9000
CMD ["php-fpm", "-F"]
