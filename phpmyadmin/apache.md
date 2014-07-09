# Apache 优化

apache MPM模式

    Apache2.0中MPM分为3种（perfork、worker、event） 
    使用apache2 -l可以查看使用哪个模式
    
了解prefork
 
    # prefork MPM
    # StartServers: number of server processes to start
    # MinSpareServers: minimum number of server processes which are kept spare
    # MaxSpareServers: maximum number of server processes which are kept spare
    # MaxClients: maximum number of server processes allowed to start
    # MaxRequestsPerChild: maximum number of requests a server process serves 
    <IfModule mpm_prefork_module>
        StartServers        30
        MinSpareServers     30
        MaxSpareServers     50
        ServerLimit         1000
        MaxClients          1000
        MaxRequestsPerChild  4000
    </IfModule>
 
## apache 优化

1.  MaxClients
    
    MaxClients ≤ ServerLimit * ThredLimit ≤ 20000 

2. Apache Memory / Process and Threads

    maxclients = total ram / ram per process
    
    list all Apache processes and number of threads per process
    
        for pid in `ps U www-data | grep apache | grep -v grep | awk '{print $1}'`;do echo Apache Worker Server $pid has \ps ms -p $pid | wc -l\` threads; done 
    
    List the reserved memory per APACHE Server and threads 
    
        #!/bin/bash
        
        servers=0
        threads=0
        space=0
        for pid in `ps U www-data | grep apache | grep -v grep | awk '{ print $1 }'`;
        do 
                process_threads=`ps ms -p $pid | wc -l`;
                process_memory=`ps -ylC -p $pid | grep -v PID | awk '{ print $8}'`;
                echo Apache Worker Server with pid $pid has $process_threads threads occupying $process_memory bytes;
                servers=`expr $servers + 1`;threads=`expr $process_threads + $threads`;space=`expr $process_memory + $space`; 
        done
        
        echo "-------------"; 
        echo Total Apache Servers: $servers \| Total threads: $threads \| Total memory reserved: $space 
        
    
