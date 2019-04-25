#!/bin/bash
images=(kube-proxy-amd64:v1.11.3 kube-scheduler-amd64:v1.11.3 kube-controller-manager-amd64:v1.11.3
kube-apiserver-amd64:v1.11.3 etcd-amd64:3.2.18 coredns:1.1.3 pause:3.1 )
for imageName in ${images[@]} ; do
docker pull anjia0532/google-containers.$imageName
docker tag anjia0532/google-containers.$imageName k8s.gcr.io/$imageName
docker rmi anjia0532/google-containers.$imageName
done
