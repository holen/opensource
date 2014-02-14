service { 
            "ssh":
             ensure => running;
            "nfs":
             ensure => stopped;
           }

