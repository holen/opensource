# swatch
install on ubuntu

    apt-cache search swatch
    apt-get install swatch

config

    vim /root/.swatchrc
        watchfor /CRON/
                echo $_

start swatch 

    swatch --config-file=/root/.swatchrc --tail-file=/var/log/syslog
