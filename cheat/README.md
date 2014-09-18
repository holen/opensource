# cheat 
##install 
install package 

    apt-get install Python
    apt-get install python-pip
    apt-get install git 
    pip install docopt pygments
    git clone https://github.com/chrisallenlane/cheat.git
    cd cheat
    python setup.py install
    cheat -v
    cheat 2.1.0

##config cheat
添加EDITOR环境变量

    vim /root/.bashrc
    export EDITOR =/usr/bin/vim  

为cheat命令添加自动补全功能

    # wget https://github.com/chrisallenlane/cheat/raw/master/cheat/autocompletion/cheat.bash
    # mv cheat.bash /etc/bash_completion.d/

高亮显示(可选)

    vim /root/.bashrc
    export CHEATCOLORS=true

添加更多的小抄(可选)

    cheat -e docker

# use cheat
list all cheat sheet

    cheat -l

list cheat dir

    cheat -d 

view command cheat

    cheat tar
    cheat ifconfig
    cheat dd
