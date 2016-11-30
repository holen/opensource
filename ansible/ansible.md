# Ansible

## Install on ubuntu 

    $ apt-get install software-properties-common
    $ apt-add-repository ppa:ansible/ansible
    $ apt-get update
    $ apt-get install ansible  
    
## Ad_Hoc command

shell

    ansible raleigh -m shell -a 'echo $TERM'
    
file transfer

    ansible atlanta -m copy -a "src=/etc/hosts dest=/tmp/hosts"
 
file chmod

    $ ansible webservers -m file -a "dest=/srv/foo/a.txt mode=600"
    $ ansible webservers -m file -a "dest=/srv/foo/b.txt mode=600 owner=mdehaan group=mdehaan"

file create and delete

    $ ansible webservers -m file -a "dest=/path/to/c mode=755 owner=mdehaan group=mdehaan state=directory"
    $ ansible webservers -m file -a "dest=/path/to/c state=absent"
    
Managing Packages

    $ ansible webservers -m yum -a "name=acme state=present"
    $ ansible webservers -m yum -a "name=acme-1.5 state=present"
    $ ansible webservers -m yum -a "name=acme state=absent"
    
Users and Groups

    $ ansible all -m user -a "name=foo password=<crypted password here>"
    $ ansible all -m user -a "name=foo state=absent"
    
Deploying From Source Control

    $ ansible webservers -m git -a "repo=git://foo.example.org/repo.git dest=/srv/myapp version=HEAD"
    
Managing Services

    $ ansible webservers -m service -a "name=httpd state=started"
    $ ansible webservers -m service -a "name=httpd state=restarted"
    $ ansible webservers -m service -a "name=httpd state=stopped"

Time Limited Background Operations

    $ ansible all -B 3600 -P 0 -a "/usr/bin/long_running_operation --do-stuff"
    $ ansible web1.example.com -m async_status -a "jid=488359678239.2844"
    $ ansible all -B 1800 -P 60 -a "/usr/bin/long_running_operation --do-stuff"
    
Gathering Facts

    $ ansible all -m setup
    
## 参考文献
[ansible中文文档](http://www.ansible.com.cn/docs/intro_adhoc.html)  
[ansible中文指南](http://www.the5fire.com/explore-the-ansible.html)  
[ansible官方文档](http://docs.ansible.com/intro_getting_started.html)  
[自动化运维工具之ansible](http://os.51cto.com/art/201409/451927_all.htm)  
