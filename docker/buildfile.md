Dockerfile用来创建一个自定义的image,包含了用户指定的软件依赖等。

当前目录下包含Dockerfile,使用命令build来创建新的image,并命名为edwardsbean/centos6-jdk1.7:
docker build -t edwardsbean/centos6-jdk1.7  .

Dockerfile关键字

如何编写一个Dockerfile,格式如下：
# CommentINSTRUCTION arguments
FROM        基于哪个镜像
RUN         安装软件用
MAINTAINER  镜像创建者
CMD         Container启动时执行的命令，但是一个Dockerfile中只能有一条CMD命令，多条则只执行最后一条CMD.
            CMD主要用于container时启动指定的服务，当Docker run command的命令匹配到CMD command时，会替换CMD执行的命令。如:

Dockerfile:

CMD echo hello world
运行一下试试:
edwardsbean@ed-pc:~/software/docker-image/centos-add-test$ docker run centos-cmd
hello world

一旦命令匹配：
edwardsbean@ed-pc:~/software/docker-image/centos-add-test$ docker run centos-cmd echo hello edwardsbean
hello edwardsbean

ENTRYPOINT

container启动时执行的命令，但是一个Dockerfile中只能有一条ENTRYPOINT命令，如果多条，则只执行最后一条
ENTRYPOINT没有CMD的可替换特性

USER
使用哪个用户跑container
如：
ENTRYPOINT ["memcached"]
USER daemon

EXPOSE
container内部服务开启的端口。主机上要用还得在启动container时，做host-container的端口映射：
docker run -d -p 127.0.0.1:33301:22 centos6-ssh
container ssh服务的22端口被映射到主机的33301端口

ENV
用来设置环境变量，比如：
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

ADD
将文件<src>拷贝到container的文件系统对应的路径<dest>
所有拷贝到container中的文件和文件夹权限为0755,uid和gid为0
如果文件是可识别的压缩格式，则docker会帮忙解压缩
    如果要ADD本地文件，则本地文件必须在 docker build <PATH>，指定的<PATH>目录下
    如果要ADD远程文件，则远程文件必须在 docker build <PATH>，指定的<PATH>目录下。
    比如:
         docker build github.com/creack/docker-firefox
         docker-firefox目录下必须有Dockerfile和要ADD的文件
         注意:使用docker build - < somefile方式进行build，是不能直接将本地文件ADD到container中。只能ADD url file.
        ADD只有在build镜像的时候运行一次，后面运行container的时候不会再重新加载了。

VOLUME
可以将本地文件夹或者其他container的文件夹挂载到container中。

WORKDIR
切换目录用，可以多次切换(相当于cd命令)，对RUN,CMD,ENTRYPOINT生效

ONBUILD
ONBUILD 指定的命令在构建镜像时并不执行，而是在它的子镜像中执行
