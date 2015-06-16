# Install lastest version git on ubuntu 12.04  
  
	apt-add-repository ppa:git-core/ppa  
	apt-get update  
	apt-get install git  
	git --version  
	git config --global user.name "hello"  
	git config --global user.email "zhl@sina.com"  
  
# Git global setup:  
  
	ssh-keygen -t rsa -C "zhl@sina.com"  
	回到github，进入Account Settings，左边选择SSH Keys，Add SSH Key,title随便填，粘贴key  
	$ ssh -T git@github.com  
	如果是第一次的会提示是否continue，输入yes就会看到：You’ve successfully authenticated, but GitHub does not provide shell access 。这就表示已成功连上github。  
  
	git config --global user.name "Administrator"  
	git config --global user.email "admin@local.host"  
    git config --global color.ui true
    git config --list
    git status -s
    git diff                # work diff staged
    git diff --staged       # staged diff HEAD(history)
    git diff HEAD           # work diff HEAD(history)
    git diff --stat HEAD
    git reset file          # HEAD reset to staged
    git checkout file       # get file from staged to work
    git chechout HEAD file  # get file from HEAD to work
    git commit -am 'add new code'  # work add to HEAD
    git rm file             # delete file 
    git rm --cached file    # delete file and file also in work
    git reset file      
    git status -s 
    git mv file file2       # rename file
    git stash               # 暫存work
    git stash list
    git stash pop           # 提取file
    git status -s 
    git log
    git log --oneline
    git cat-file -t HEAD
    git cat-file -p HEAD
    git rev-parse HEAD
    git rev-parse HEAD~
    git rev-parse HEAD~4
    git rev-parse master~4
    git rev-parse HEAD~4^{tree}
    git rev-parse HEAD~4:code.py
    git cat-file -p HEAD~4:code.py
    git show -p HEAD~4:code.py
  
# Create Repository  
  
    mkdir bash  
    cd bash  
    touch README.md  
    git init  
    git add README.md               # work add to staged
    git status
    git commit -m "first commit"    # staged commit to HEAD
    git remote add origin https://github.com/holen/bash.git  
    git remote -v  
    git push -u origin master  

# create branch

    git branch
    git branch tryidea      # create tyrieda branch
    git branch
    git checkout tryidea    # switch to tryidea分支
    git branch
    git checkout master
    git branch -d tryidea   # delete tryidea branch
    git checkout -b tryidea   # create and switch to new branch
    git merge tryidea       # merge branch to master

three way merge

    git checkout -b bugfix
    modify
    git commit -am "bug fix"
    git checkout master
    modify
    git merge bugfix
