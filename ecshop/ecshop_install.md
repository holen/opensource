# install on ubuntu
install mysql apache php5

    apt-get install mysql apache2 php5 php5-gd php5-mysql 

download ecshop

    wget http://download.ecshop.com/2.7.3/ECShop_V2.7.3_UTF8_release1106.rar

unrar .rar file

    unrar x ECShop_V2.7.3_UTF8_release1106.rar /opt/
    mv ECShop_V2.7.3_UTF8_release1106 ecshop
    ln -s /opt/ecshop/upload /var/www/ecshop
    chown -R www-data.www-data ecshop
    chmod 777 /var/www/ecshop -R
    service apache2 restart

access install web

    http://ip/ecshop/

JPEG不支持

    vim install/includes/lib_installer.php
    将$gd_info['JPG Support'] 修改为$gd_info['JPEG Support']即可

##参考文献
[JPEG不支持](http://www.haowt.info/archives/230.html)  
[unbunt install ecshop](http://www.cnblogs.com/candycaicai/p/3611731.html)  
