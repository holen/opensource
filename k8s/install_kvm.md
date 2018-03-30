# KVM Virtualization in RHEL 7 Made Easy    
ref http://linux.dell.com/files/whitepapers/KVM_Virtualization_in_RHEL_7_Made_Easy.pdf
ref https://github.com/kubernetes/minikube/blob/master/docs/drivers.md#kvm2-driver

# kvm

    yum install qemu-kvm libvirt libvirt-python libguestfs-tools virt-install
    https://github.com/dhiltgen/docker-machine-kvm/releases
    minikube start --vm-driver kvm

# kvm 2

    yum install libvirt-daemon-kvm qemu-kvm
    usermod -a -G libvirt $(whoami)
    newgrp libvirt

Basic command 

    systemctl enable libvirtd
    systemctl start libvirtd
    systemctl status libvirtd
    virsh list --all 

install the kvm2 driver

    curl -LO https://storage.googleapis.com/minikube/releases/latest/docker-machine-driver-kvm2 && chmod +x docker-machine-driver-kvm2 && sudo mv docker-machine-driver-kvm2 /usr/bin/

To use the driver you would do:

    minikube start --vm-driver kvm2
