# Install lastest version git on ubuntu 12.04  
  
	apt-add-repository ppa:git-core/ppa  
	apt-get update  
	apt-get install git  
	git --version  
	git config --global user.name "holen"  
	git config --global user.email "yh_zhl@sina.com"  
  
# Git global setup:  
  
	ssh-keygen -t rsa -C "yh_zhl@sina.com"  
	回到github，进入Account Settings，左边选择SSH Keys，Add SSH Key,title随便填，粘贴key  
	$ ssh -T git@github.com  
	如果是第一次的会提示是否continue，输入yes就会看到：You’ve successfully authenticated, but GitHub does not provide shell access 。这就表示已成功连上github。  
  
	git config --global user.name "Administrator"  
	git config --global user.email "admin@local.host"  
  
# Create Repository  
  
    mkdir bash  
    cd bash  
    touch README.md  
    git init  
    git add README.md  
    git commit -m "first commit"  
    git remote add origin https://github.com/holen/bash.git  
    git remote -v  
    git push -u origin master  
