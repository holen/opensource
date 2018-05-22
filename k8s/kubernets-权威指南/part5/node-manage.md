# Node 的隔离与恢复
剔除Node

    kubectl patch node k8s-node-1 -p '{"spec":{"unschedulable":true}}'
    or
    kubectl cordon k8s-node-1

恢复

    kubectl uncordon k8s-node-1

# Node 的扩容 

在新节点Node上安装 docker,kubectl和Kube-proxy服务，然后配置kubectl 和 kubectl-proxy 的启动参数，将Master URL指定为当前Kubernetes集群的Master地址。


# 更新Label
创建Label

    kubectl label pod redis-master-bobr0 role=backend
    kubectl get pods -Lrole

删除Label

    kubectl label pod redis-master-bobr0 role-

修改label

    kubectl label pod redis-master-bobr0 role=master --overwrite

