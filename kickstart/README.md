# Kickstart install ubuntu12.04

linux安装大致可以分为2个阶段
第一阶段：anaconda 阶段
此阶段是linux的预安装环境，提供linux安装选项的一个接口，可以将它比作是window中的PE环境
第二阶段：install 阶段
该阶段系统会按照anaconda 阶段设定的参数自动安装
 
    anaconda有两种模式：
    交互式：和普通安   装一样，按照提示选择选项一步步的安装
    非交互式：通过读取kickstart文件的配置，进行自动安装
    而在安装linux过程中，获取ks.cfg文件的方式有多种，如直接在cdrom中获取，常见的形式还有http，ftp，nfs等方式
    cdrom和硬盘：
    ks=cdrom:/dir/ks.cfg
    ks=hd:/dir/ks.cfg
    http和ftp：
    ks=http://domain.com/dir/ks.cfg
    ks=ftp://domain.com/dir/ks.cfg
    NFS：
    ks=nfs:domain.com:/dir/ks.cfg

    在使用ks.cfg之前，需要先引导启动环境，引导方式有cdrom、usb、PXE等。
    在引导进入anaconda后，即可通过读取ks.cfg来进行系统的自动安装 ks.cfg文件会在安装linux后，根据用户的安装选项自动生成在root家目录，即anaconda_ks.cfg ks.cfg文件组成大致分为3段
    1.命令段：
    键盘类型，语言，安装方式等系统的配置，有必选项和可选项，如果缺少某项必选项，安装时会中断并提示用户选择此项的选项
    2.软件包段：
    %packages
    @groupname        #指定安装的包组
        package_name            #指定安装的包
        -package_name        #指定安装的包
        3.脚本段(可选)：
        %pre :预安装脚本        （由于只依赖于启动镜像，支持的命令很少）
        %post:后安装脚本（基本支持所有命令）    

    %post
    apt-get update
    mkdir /home/user

# Auto install

## Install system-config-kickstart

    $ apt-cache search kickstart
    $ apt-get install system-config-kickstart
    $ system-config-kickstart # 这会提供一个图形界面进行相应的参数设置
    
    设置完kickstart,把文件保存为ks.cfg。如果有必要的话可以对该文件进行编辑 

## Extract ubuntu iso 
    下载ubuntu ISO 镜像，并进行解压。解压如下：

    mkdir /mnt/iso
    mount -o loop  ubuntu-12.04.3-server-amd64.iso /mnt/iso
    mkdir /data/autoiso
    cp -r /mnt/iso /data/autoiso/
    cd /data/autoiso/iso/
    cp /path/to/ks.cfg .
    chmod 755 isolinux/txt.cfg
    vim isolinux/txt.cfg # 在末尾加上以下内容
    label autoinstall
    menu label ^Auto install
    kernel /install/vmlinuz
    append  file=/cdrom/preseed/ubuntu-server.seed initrd=/install/initrd.gz ks=cdrom:/ks.cfg

## Compress iso

    cd /data/autoiso/iso/
    mkisofs -r -V "$IMAGE_NAME" -cache-inodes -J -l -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o  /data/autoiso/autoinstall.iso .  
    # -o参数是指定做好的iso放置的目录，这个指令的最后面有一个個“.”，太小了，很容易会遗忘它的存在。
    mkisofs完后，/data/autoiso/下会多个autoinstall.iso文件，现在就可以使用autoinstall.iso镜像进行自动化安装
    md5sum -c md5sum.txt # 验证文件
    使用该镜像安装ubuntu系统，在开机界面选择Auto install系统就会自动安装完成

## 参考文献

    http://fedoraproject.org/wiki/Anaconda/Kickstart#bootloader  
    http://fedoraproject.org/wiki/Anaconda/Kickstart/zh-cn#part_or_partition.28.E5.BF.85.E9.9C.80.29
