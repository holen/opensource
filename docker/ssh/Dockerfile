# sshd
# 

FROM ubuntu:12.04
MAINTAINER zhl

# make surre the package repository is up to date 
RUN apt-get update

RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:qwer1234' | chpasswd

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
