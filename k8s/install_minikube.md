# Installation
ref: https://github.com/kubernetes/minikube/releases     
ref: https://kubernetes.io/docs/tasks/tools/install-minikube/    
Minikube is a tool that makes it easy to run Kubernetes locally. Minikube runs a single-node Kubernetes cluster inside a VM on your laptop for users looking to try out Kubernetes or develop with it day-to-day.

Before you begin

    VT-x or AMD-v virtualization must be enabled in your computer’s BIOS.

Install a Hypervisor

    install_kvm.md

Install kubectl

    install_kubectl.md

Install Minikube

    # curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.1/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
    curl -Lo minikube http://kubernetes.oss-cn-hangzhou.aliyuncs.com/minikube/releases/v0.25.2/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/

