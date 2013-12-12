#一：准备软件包，存放/home/xiutuo/software/目录下。  
  
##主要软件包，其他版本的安装方法也类似  
  
1. httpd-2.2.6.tar.gz  
  
2. mysql-5.0.45-linux-i686-glibc23.tar.gz  
  
3. php-5.2.5.tar.gz  
  
##安装php所需的软件包（其中libxml2是安装php5必须的.）  
  
1. libxml2-(version).tar.gz  --->  http://ftp.gnome.org/pub/GNOME/sources/libxm2  
$ yum install libxml2-python.x86_64 libxml2-static.x86_64 libxml2.x86_64 libxml2-devel.x86_64  
  
2. libxslt-(version).tar.gz  --->  http://ftp.gnome.org/pub/GNOME/sources/libxslt  
  
3. curl-(version).tar.gz     --->  http://curl.haxx.se/download  
wget http://curl.haxx.se/download/curl-7.15.0.tar.gz  
  
##GD库所需要软件包（有人说PHP源码包里自带了GD2.0.28和zlib，只要安装GD的三个支持包：jpg,png和freetype，但是我们还是下载）  
  
1. gd-(version).tar.gz       --->  http://www.libgd.org/Main_Page  or  http://www.libgd.org/releases/  
  
2. freetype-(version).tar.gz --->  http://sourceforge.net/projects/freetype  
wget http://sourceforge.net/projects/freetype/files/latest/download  
  
3. jpegsrc.v6b.tar.gz        --->  http://ijg.org/files/jpegsrc.v6b.tar.gz  
wget http://ijg.org/files/jpegsrc.v6b.tar.gz  
  
4. libpng-(version).tar.gz   --->  http://www.libpng.org/pub/png/libpng.html  
wget http://downloads.sourceforge.net/project/libpng/libpng16/1.6.7/libpng-1.6.7.tar.gz?r=http%3A%2F%2Fwww.libpn  
g.org%2Fpub%2Fpng%2Flibpng.html&ts=1386746024&use_mirror=jaist  
  
5. zlib-1.2.3.tar.gz         --->  http://www.zlib.net  
wget http://zlib.net/zlib-1.2.8.tar.gz  
  
把以上所有软件包下载到：/root/Software/目录下.  
  
  
#二：安装mysql  
  
  
$ tar -zvxf mysql-5.0.45-linux-i686-glibc23.tar.gz    
  
$ mkdir -p /usr/local/mysql  
  
$ cp -r mysql-5.0.45 /usr/local/mysql  
  
$ cp /usr/local/mysql/support-files/mysql.server /etc/rc.d/init.d/mysql //开机启动mysql  
  
$ cp /usr/local/mysql/support-files/my-medium.cnf /etc/my.cnf  
  
  
添加mysql用户及用户组  
  
$ groupadd mysql  
  
$ useradd -g mysql mysql  
  
修改mysql目录权限  
  
$ chown -R root /usr/local/mysql  
  
$ chgrp -R mysql /usr/local/mysql  
  
$ chown -R mysql /usr/local/mysql/data  
  
生成mysql系统数据库  
  
$ /usr/local/mysql/.s/mysql_install_db --user=mysql&  //启动mysql服务  
  
$ /usr/local/mysql/bin/mysqld_safe --user=mysql&  
  
如出现 Starting mysqld daemon with databases from /usr/local/mysql/data 代表正常启动mysql服务了.  
  
按Ctrl + C 跳出修改 mysql 的 root 密码  
  
$ /usr/local/mysql/bin/mysqladmin -u root -p password "123456"  
  
  
# 三：安装GD库(让PHP支持GIF,PNG,JPEG)  
  
##a.安装 jpeg6 建立目录：  
  
$ mkdir -p /usr/local/jpeg6  
$ mkdir -p /usr/local/jpeg6/bin  
$ mkdir -p /usr/local/jpeg6/lib  
$ mkdir -p /usr/local/jpeg6/include  
$ mkdir -p /usr/local/jpeg6/man  
$ mkdir -p /usr/local/jpeg6/man1  
$ mkdir -p /usr/local/jpeg6/man/man1  
$ cd /root/Software/  
  
yum install libtool-ltdl-devel.x86_64  
wget http://ftp.gnu.org/gnu/libtool/libtool-2.2.6a.tar.gz  
tar xvfz libtool-2.2.6a.tar.gz  
cd libtool-2.2.6  
./configure --prefix=/usr/local/libtool && make && make install  
  
$ tar -zvxf jpegsrc.v6b.tar.gz  
  
$ cd jpeg6  
cp /usr/local/libtool/config/config.sub .  
cp /usr/local/libtool/config/config.guess .  
$ ./configure --prefix=/usr/local/jpeg6/ --enable-shared --enable-static  
$ make  
$ make install  
  
  
##b.libpng包(支持PNG)  
  
$ cd /root/Software/  
  
$ tar -zvxf libpng-(version).tar.gz  
  
$ cd libpng-(version)  
$ ./configure --prefix=/usr/local/libpng  
$ make  
$ make install  
  
  
##c.安装 freetype  
  
$ cd /root/Software/  
  
$ tar -zvxf freetype-(version).tar.gz  
$ cd freetype-(version)  
$ mkdir -p /usr/local/freetype  
$ ./configure --prefix=/usr/local/freetype  
$ make  
$ make install  
  
  
## d.安装zlib  
  
$ cd /root/Software/  
  
$ tar -zxvf zlib-1.2.3.tar.gz  
$ cd zlib.1.2.3  
$ mkdir /usr/local/zlib  
$ ./configure --prefix=/usr/local/zlib  
$ make  
$ make install  
  
  
## e.安装GD库  
  
$ cd /root/Software/  
  
$ tar zxvf gd-2.0.33.tar.gz  
$ mkdir -p /usr/local/gd2  
$ cd gd-(version)  
$ ./configure --prefix=/usr/local/gd2 --with-jpeg=/usr/local/jpeg6 --with-zlib-dir=/usr/local/zlib --with-png=/usr/local/libpng --with-freetype=/usr/local/freetype  
vim /root/software/gd-2.0.33/gd_png.c  
$include "/usr/local/libpng/include/png.h"  
$ make  
$ make install  
  
  
## e.安装Curl库  
  
$ cd /root/Software/  
  
$ tar -zxf curl-(version).tar.gz  
$ mkdir -p /usr/local/curl  
$ ./configure --prefix=/usr/local/curl  
$ make  
$ make install  
  
  
# 四：安装apache2  
wget http://mirrors.hust.edu.cn/apache//apr/apr-1.5.0.tar.gz  
wget http://archive.apache.org/dist/apr/apr-util-1.5.3.tar.gz  
wget http://downloads.sourceforge.net/project/pcre/pcre/8.33/pcre-8.33.tar.bz2?r=http%3A%2F%2Fsourceforge.net%2F  
  projects%2Fpcre%2F&ts=1386753328&use_mirror=softlayer-ams  
  
tar zxvf apr-1.5.0.tar.gz   
cd apr-1.5.0  
./configure --prefix=/usr/local/apr   
make  
make install   
  
cd ..  
tar zxvf apr-util-1.5.3.tar.gz   
cd apr-util-1.5.3  
./configure --prefix=/usr/local/apr-util -with- apr=/usr/local/apr/bin/apr-1-config   
./configure --prefix=/usr/local/apr-util -with-apr=/usr/local/apr/bin/apr-1-config   
make  
make install   
  
cd ..  
tar jxvf pcre-8.33.tar.bz2   
cd pcre-8.33  
./configure --prefix=/usr/local/pcre    
make   
make install  
  
  
$ cd /roo/Software/  
  
wget http://apache.fayea.com/apache-mirror//httpd/httpd-2.2.26.tar.gz  
  
$ tar -zvxf httpd-2.2.6.tar.gz  
$ cd httpd-2.2.6  
$ mkdir -p /usr/local/apache2  
./configure --prefix=/usr/local/apache2 --enable-modules=all --enable-rewrite --with-apr=/usr/local/apr/ --with-apr-util=/usr/local/apr-util/ --with-pcre=/usr/local/pcre  
$ make  
$ make install    
  
$ /usr/local/apache2/bin/apachectl -k start //启动apahce  
  
用浏览器查看http://localhost,得到it works，说明apache已经配置成功了.  
  
$ /usr/local/apache2/bin/apachectl -k stop  //停止apache  
  
# 五：安装php5，php5必须有libxml2支持!  
  
## a. 安装libxml2  
  
$ cd /root/Software/  
  
yum install libxml2-devel.x86_64 gd-devel  
  
$ tar -zvxf libxml2-(version).tar.gz  
$ cd libxml2-(version)  
$ mkdir -p /usr/local/libxml2  
$ ./configure --prefix=/usr/local/libxml2  
$ make  
$ make install  
  
  
## b.安装 libxslt (可选安装，你可以不安装)  
  
$ cd /root/Software/  
  
$ tar -zvxf libxslt-(version).tar.gz  
$ mkdir -p /usr/local/libxslt  
$ cd libxslt-(version)  
$ ./configure --prefix=/usr/local/libxslt --with-libxml-prefix=/usr/local/libxml2  
$ make  
$ make install  
  
  
## c.安装php5  
  
$ cd /root/Software/  
$ tar -zvxf php-(version).tar.gz  
$ mkdir -p /usr/local/php5  
$ cd php-(version)  
./configure --prefix=/usr/local/php5 \   
--with-apxs2=/usr/local/apache2/bin/apxs --with-mysql \   
--with-libdir=lib64 --with-gd=/usr/local/gd2 \   
--with-jpeg-dir=/usr/local/jpeg6 --with-zlib-dir=/usr/local/zlib \  
--with-png-dir=/usr/local/libpng --with-freetype-dir=/usr/local/freetype \  
--enable-mbstring=all --with-curl=/usr/local/curl --enable-mbregex \  
--with-config-file-path=/usr/local/php5 --enable-ftp --enable-soap \  
--with-xsl=/usr/local/libxslt --with-libxml-dir=/usr/local/libxml2  
$ make  
$ make install  
  
$ cp php.ini-dist /usr/local/php5/php.ini  （别忘记了呵呵）  
  
  
# 六：重新配置apache2让他支持php  
  
  
$ cd /usr/local/apache2/conf  
  
$ vim httpd.conf  
  
在LoadModule php5_module modules/libphp5.so  
  
添加AddType application/x-httpd-php  .php  
  
  
OK,基本的安装已经完成.  
  
重新起动APACHE:  
  
$ /usr/local/apache2/bin/apachectl start  
  
# 七、安装ZendOptimizer-3.3  
  
 wget http://downloads.zend.com/optimizer/3.3.3/ZendOptimizer-3.3.3-linux-glibc23-x86_64.tar.gz  
tar zxvf ZendOptimizer-3.3.3-linux-glibc23-x86_64.tar.gz   
cd ZendOptimizer-3.3.3-linux-glibc23-x86_64  
./install.sh   
  
