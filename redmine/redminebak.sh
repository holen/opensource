#!/bin/bash

Mysqldump="/opt/redmine-2.3.1-0/mysql/bin/mysqldump"
Rsync=`which rsync`
Date=`date +%Y%m%d`

$Mysqldump -uroot -p'w.cn@mysql@' --events --all-databases | gzip > /data/backup/redmine-zdcpb/redmine.${Date}.sql.gz
tar zcvf /backup/redmine.${Date}.tgz /opt/redmine-2.3.1-0/apps/redmine
$Rsync -av /backup/ root@10.0.120.22:/data/backup/redmine/

find /backup/* -mtime +7 | xargs -I {} rm {}   
