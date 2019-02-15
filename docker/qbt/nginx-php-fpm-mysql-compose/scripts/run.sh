#!/bin/bash

chown -R www.www /data/web/yii2

php /data/web/yii2/init --env=Development --overwrite=All

sed -i -e 's/localhost/mysqldb/g' -e 's/yii2advanced/yii2/g' -e 's/root/yii/g' -e "s/'password' => ''/'password' => 'Yii123456'/g" /data/web/yii2/common/config/main-local.php

/data/web/yii2/yii migrate --interactive=0
