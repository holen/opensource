# migrate
backup

    /opt/redmine-2.3.1-0/mysql/bin/mysqldump -ubn_redmine -p'6e7363e4d7' --events --all-databases > /backup/redmine.sql
    tar zcvf /backup/redmine.tgz /opt/redmine-2.3.1-0/apps/redmine
    tar zcvf /backup/apache.tgz /opt/redmine-2.3.1-0/apache2

restore mysql

    vim my.cnf
    skip-grant-table
    ./bin/mysql -uroot -p
    update user set password=password('qwer1234') where user = 'root';
    flush privileges;
    grant all privileges on bitnami_redmine.* to bn_redmine@'localhost' identified by '6e7363e4d7';
    grant all privileges on bitnami_redmine.* to bitnami@'localhost' identified by '7e29fb7066';
    ./bin/mysql -ubitnami -p bitnami_redmine < /tmp/redmine.sql

restore apps 

    tar zxvf redmine.tgz
    rsync -av /tmp/opt/redmine-2.3.1.-0/redmine/ /opt/redmine-2.3.1-0/apps/redmine/
    tar zxvf apache.tgz
    rsync -av /tmp/apache2/conf/ /opt/redmine-2.3.1-0/apache2/conf/
