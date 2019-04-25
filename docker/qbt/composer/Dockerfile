FROM qianbitou/php70-fpm:1.1

RUN ln -s /usr/local/webserver/php-70/bin/php /usr/bin/ \
    && php -r "copy('https://install.phpcomposer.com/installer', 'composer-setup.php');" \
    && php composer-setup.php \
    && php -r "unlink('composer-setup.php');" \
    && mv composer.phar /usr/local/bin/composer \
    && composer config -g repo.packagist composer https://packagist.phpcomposer.com \
    && ln -s /usr/local/bin/composer /usr/bin/ \
    && mkdir /home/www \
    && chown -R www.www /home/www


# COPY docker-entrypoint.sh /docker-entrypoint.sh

# ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]
# CMD ["composer"]

WORKDIR /home/www/app

USER www

# RUN composer config -g repo.packagist composer https://packagist.phpcomposer.com \
#     && composer install

CMD ["-"]

ENTRYPOINT ["composer", "--ansi"]
