# 从一个小应用开始
建一个mysql-rc.yml文件

启动mysql服务

    [root@localhost get_start]# kubectl create -f mysql-rc.yml 
    replicationcontroller "mysql" created

查看刚刚创建的RC

    [root@localhost get_start]# kubectl get rc
    NAME      DESIRED   CURRENT   READY     AGE
    mysql     1         1         0         4m

查看pod

    [root@localhost get_start]# kubectl get pod
    NAME          READY     STATUS              RESTARTS   AGE
    mysql-5q25h   0/1       ContainerCreating   0          4m

    [root@localhost ~]# kubectl get pods
    NAME          READY     STATUS    RESTARTS   AGE
    mysql-5q25h   1/1       Running   0          3d

    $ docker ps | grep mysql 
    6e5ed386ca66        mysql                                                                             "docker-entrypoint.s…"   3 days ago          Up 3 days                               k8s_mysql_mysql-5q25h_default_3565f8e5-4ac4-11e8-a115-90cbc622e6ac_0
    3f8132f46372        k8s.gcr.io/pause-amd64:3.1                                                        "/pause"                 3 days ago          Up 3 days                               k8s_POD_mysql-5q25h_default_3565f8e5-4ac4-11e8-a115-90cbc622e6ac_0

创建一个与之相关联的kubernetes service

    [root@localhost get_start]# kubectl create -f mysql-svc.yml 
    service "mysql" created

    [root@localhost get_start]# kubectl get svc
    NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)     AGE
    kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP     3d
    mysql        ClusterIP   10.106.138.109   <none>        33061/TCP   1m

启动tomcat web应用

    [root@localhost get_start]# kubectl create -f myweb-rc.yml 
    replicationcontroller "myweb" created

