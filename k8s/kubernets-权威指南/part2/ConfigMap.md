# ConfigMap 容器应用的配置管理
创建ConfigMap

    [root@localhost get_start]# kubectl create -f cm-appvars.yml 
    configmap "cm-appvars" created

Use kubectl
通过--from-file参数从目录中进行创建，该目录下的每个配置文件名都被设置为Key,文件内容被设置为value

	kubectl create configmap Name --from-file=[key=]source --from-file=[key=]source

--from-literal从文本中进行创建，直接将指定的key#=value#创建为ConfigMap的内容

	kubectl create configmap NAME --from-literal=key1=value1 --from-literal=key2=value2

查看

    [root@localhost get_start]# kubectl get configmap
    NAME         DATA      AGE
    cm-appvars   2         54s
    
    [root@localhost get_start]# kubectl describe configmap cm-appvars 
    Name:         cm-appvars
    Namespace:    default
    Labels:       <none>
    Annotations:  <none>

    Data
    ====
    appdatadir:
    ----
    /var/data
    apploglevel:
    ----
    info
    Events:  <none>

	[root@localhost get_start]# kubectl get configmap -o yaml         

