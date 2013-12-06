# resume
CheckInstall能跟踪由“make install”或类似命令安装的所有文件，并为这些文件创建Slackware、RPM或者Debian安装包，然后把它添加到已安装软件包数据库中，以便能简便的卸载或发布安装包。 

# install 
apt-get install checkinstall -y

# 通过 auto-apt 使用 CheckInstall

当你想用 checkinstall 从源码建立一个简单的软件包，你可以使用 auto-apt 。你需要安装 auto-apt ！

代替：

/configure

你可使用：

auto-apt run ./configure

如果有可用的依赖包，会弹出一个对话框，让你安装他们。

接着的步骤就一样了：

make
sudo checkinstall

