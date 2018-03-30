# Running Kubernetes Locally via Minikube

Quickstart

    [root@localhost opt]# minikube start --vm-driver kvm2
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

    # ref http://docs.kubernetes.org.cn/317.html
    [root@localhost opt]# kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.4 --port=8080
    deployment "hello-minikube" created

    [root@localhost opt]# kubectl expose deployment hello-minikube --type=NodePort
    service "hello-minikube" exposed

    [root@localhost opt]# kubectl get pod
    NAME                            READY     STATUS              RESTARTS   AGE
    hello-minikube-c6c6764d-28wjp   0/1       ContainerCreating   0          27s

    
