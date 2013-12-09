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
  
  在使用ks.cfg之前，需要先引导启动环境，引导方式有cdrom、usb、PXE等。在引导进入anaconda后，即可通过读取ks.cfg来进行系统的自动安装 ks.cfg文件会在安装linux后，根据用户的安装选项自动生成在root家目录，即anaconda_ks.cfg ks.cfg文件组成大致分为3段
  1.命令段：
  键盘类型，语言，安装方式等系统的配置，有必选项和可选项，如果缺少某项必选项，安装时会中断并提示用户选择此项的选项
  2.软件包段：
  %packages
  @groupname        #指定安装的包组
    package_name            #指定安装的包
    -package_name        #指å不安装的包
    3.脚本段(可选)：
    %pre :预安装脚本        （由于只依赖于启动镜像，支持的命令很少）
    %post:后安装脚本（基本支持所有命令）    

