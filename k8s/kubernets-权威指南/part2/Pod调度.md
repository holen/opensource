# Pod 调度

RC、Deployment 全自动高度

NodeSelector 定向调度
首先通过Kubectl label命令给目标Node打上标签

    kubectl label nodes <node-name> <label-key>=<label-value>
    kubectl label nodes node-1 zone=north
    or
    kubectl replace -f xxx.yml

在Pod中定义加上nodeSelector的设置

    spec.template.spec.nodeSelector.zone: north

查看

    kubectl get pods -o wide

NodeAffinity 亲和性调度
