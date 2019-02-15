# 介绍

利用 docker-compose 安装 yii2-advanced 的 lnmp 环境

# 安装 

	git clone 项目到当前目录
    下载最新的 yii2-advanced 包，解压到 docker-compose.yml 同目录 

# 登录 docker hub ，启动服务

    docker login
    docker-compose up -d 

# 初始化项目，配置数据库信息，同步数据库

    docker-compose exec php bash /root/run.sh

# yii2 配置 

前端	对应 8000端口
后端	对应 8001端口

访问：

	127.0.0.1:8000
	127.0.0.1:8001


