# 在 node-1 上执行
mkdir -p /mnt/disks
for vol in vol1 vol2 vol3; 
do
    mkdir -p /mnt/disks/$vol
    mount -t tmpfs $vol /mnt/disks/$vol
done

