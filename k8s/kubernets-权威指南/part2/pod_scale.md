# Pod 扩容与缩容
将redis-slave RC控制的Pod副本数量从初始的2更新为3

    kubectl scale rc redis-slave --replicas=3

# HPA (Horizontal Pod Autoscale) 
需在 RC 或 Deployment 对象中的Pod 定义resources.requests.cpu 的资源请求值 

为RC "php-apache"创建一个HPA控制器，在1和10之间调整Pod的副本数量

    kubectl autoscale rc php-apache --min=1 --max=10 --cpu-percent=50

    kubectl create -f hpa-php-apache.yml

    kubectl get hpa

# rolling-update
版本升级

    kubectl rolling-update redis-master --image=redis-master:2.0

升级报错回滚

    kubectl rolling-update redis-master --image=redis-master:2.0 --rollback
