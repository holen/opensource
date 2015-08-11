# Install rabbitmq on ubuntu 12.04

Customise the RabbitMQ environment

    vim /etc/rabbitmq/rabbitmq-env.conf 
    NODENAME=bunny@localhost
    CONFIG_FILE=/etc/rabbitmq/testdir/bunnies

Install

    echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list
    wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
    apt-key add rabbitmq-signing-key-public.asc
    apt-get install rabbitmq-server

Install RabbitMQ libraries

    apt-get install python-pip git-core
    pip install pika==0.9.8

Command

    rabbitctl status
    rabbitctl list_queues
    rabbitmqctl list_queues name messages_ready messages_unacknowledged
    rabbitmqctl list_exchanges
    rabbitmqctl list_bindings
