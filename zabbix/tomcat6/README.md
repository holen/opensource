# Zabbix monitor tomcat6
Zabbix Server install zabbix-java-gateway

    apt-get install zabbix-java-gateway 

vim /etc/zabbix/zabbix_java_gateway.conf

    LISTEN_IP="10.0.1.11"
    LISTEN_PORT=10052
    PID_FILE="/var/run/zabbix/zabbix_java_gateway.pid"
    START_POLLERS=5 

vim /etc/zabbix/zabbix_server.conf 

    JavaGateway=10.0.1.11 
    JavaGatewayPort=10052 
    StartJavaPollers=5 

`/etc/init.d/zabbix-java-gateway restart`  
`/etc/init.d/zabbix-server restart`  

netstat -tunlp | grep 10052

    tcp6       0      0 10.0.1.11:10052       :::*                    LISTEN      20984/java 
    
Zabbix agent install tomcat6
    
    apt-get install tomcat6 
    
vim /etc/default/tomcat6 

    JAVA_OPTS="-Djava.awt.headless=true -Xmx128m -XX:+UseConcMarkSweepGC -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.port=5555 -Djava.rmi.server.hostname=10.0.1.42" 
    
`service tomcat6 restart`  

Modify tomcat host web gui

    add JMX interface : IP --> 10.0.1.42  Port --> 5555
    
Link tomcat template
