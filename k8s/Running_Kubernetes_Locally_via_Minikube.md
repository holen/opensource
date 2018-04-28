# Running Kubernetes Locally via Minikube

Quickstart

    [root@localhost opt]# minikube start --vm-driver kvm2 --docker-env http_proxy=$http_proxy --docker-env https_proxy=$https_proxy
    There is a newer version of minikube available (v0.25.2).  Download it here:
    https://github.com/kubernetes/minikube/releases/tag/v0.25.2
    
    To disable this notification, run the following:
    minikube config set WantUpdateNotification false
    Starting local Kubernetes v1.9.0 cluster...
    Starting VM...
    Getting VM IP address...
    Moving files into cluster...
    Downloading localkube binary
     162.41 MB / 162.41 MB [============================================] 100.00% 0s
     0 B / 65 B [----------------------------------------------------------]   0.00%
     65 B / 65 B [======================================================] 100.00% 0sSetting up certs...
    Connecting to cluster...
    Setting up kubeconfig...
    Starting cluster components...
    Kubectl is now configured to use the cluster.
    Loading cached images from config file.

	# ref: http://docs.kubernetes.org.cn/126.html
    设置Minikube 环境。可以在~/.kube/config文件中查看所有可用的环境 。
    [root@localhost node]# kubectl config use-context minikube
    Switched to context "minikube".

    验证kubectl配置：
    kubectl cluster-info

    创建Node.js应用程序
    server.js
	var http = require('http');

	var handleRequest = function(request, response) {
	  console.log('Received request for URL: ' + request.url);
	  response.writeHead(200);
	  response.end('Hello World!');
	};
	var www = http.createServer(handleRequest);
	www.listen(8080);

	运行应用：
	node server.js

	创建Docker容器镜像
	Dockerfile 

	FROM node:6.9.2

    FROM registry.cn-hangzhou.aliyuncs.com/kong/node6.9.2
	EXPOSE 8080
	COPY server.js .
	CMD node server.js

	eval $(minikube docker-env)

	使用Minikube Docker守护进程build Docker镜像：
	docker build -t hello-node:v1 .

	创建Deployment
	使用kubectl run命令创建Deployment来管理Pod。Pod根据hello-node:v1Docker运行容器镜像：
	[root@localhost node]# kubectl run hello-node --image=hello-node:v1 --port=8080
	deployment "hello-node" created

	查看Deployment：
    [root@localhost node]# kubectl get deployments
    NAME         DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
    hello-node   1         1         1            1           24s
    $ kubectl describe deployments

	查看Pod:
    [root@localhost node]# kubectl get pods
    NAME                          READY     STATUS    RESTARTS   AGE
    hello-node-658d8f6754-w86n6   1/1       Running   0          11s

	查看群集events：
	kubectl get events

	查看kubectl配置：
	kubectl config view

	创建Service
	默认情况，这Pod只能通过Kubernetes群集内部IP访问。要使hello-node容器从Kubernetes虚拟网络外部访问，须要使用Kubernetes Service暴露Pod。

	我们可以使用kubectl expose命令将Pod暴露到外部环境：
	[root@localhost node]# kubectl expose deployment hello-node --type=LoadBalancer
	service "hello-node" exposed

	查看刚创建的Service：
	[root@localhost node]# kubectl get services
	NAME         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
	hello-node   LoadBalancer   10.96.36.111   <pending>     8080:30690/TCP   29s
	kubernetes   ClusterIP      10.96.0.1      <none>        443/TCP          29m

    kubectl delete service hello-node
    kubectl delete deployment hello-node

    # ref http://docs.kubernetes.org.cn/317.html
    [root@localhost opt]# kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.4 --port=8080
    deployment "hello-minikube" created

    [root@localhost opt]# kubectl expose deployment hello-minikube --type=NodePort
    service "hello-minikube" exposed

    [root@localhost opt]# kubectl get pod
    NAME                            READY     STATUS              RESTARTS   AGE
    hello-minikube-c6c6764d-28wjp   0/1       ContainerCreating   0          27s

    
