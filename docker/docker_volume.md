# ubuntu aufs

mount -t aufs -o br=/root/dir1=ro:/root/dir2=rw none /root/aufs

devicemapper

    DOCKER_OPTS="--storage-driver=devicemapper"

Overlayfs

    DOCKER_OPTS="--storage-driver=overlay"
