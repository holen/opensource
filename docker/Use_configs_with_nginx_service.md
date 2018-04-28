# Advanced example: Use configs with a Nginx service
ref: http://docs.docker-cn.com/engine/swarm/configs/#advanced-example-use-configs-with-a-nginx-service

Configure the Nginx container  

create a new file called site.conf

	server {
    	listen                443 ssl;
    	server_name           localhost;
    	ssl_certificate       /run/secrets/site.crt;
    	ssl_certificate_key   /run/secrets/site.key;

    	location / {
    	    root   /usr/share/nginx/html;
    	    index  index.html index.htm;
    	}
	}

Create two secrets, representing the key and the certificate. 

	$ docker secret create site.key site.key
	$ docker secret create site.crt site.crt

Save the site.conf file in a Docker config

	$ docker config create site.conf site.conf
	$ docker config ls

Create a service that runs Nginx and has access to the two secrets and the config.

	$ docker service create \
     --name nginx \
     --secret site.key \
     --secret site.crt \
     --config source=site.conf,target=/etc/nginx/conf.d/site.conf \
     --publish 3000:443 \
     nginx:latest \
     sh -c "exec nginx -g 'daemon off;'"

Verify that the Nginx service is running.

	$ docker service ls
	$ docker service ps nginx

Verify that the service is operational: you can reach the Nginx server, and that the correct TLS certificate is being used.

	$ curl --cacert root-ca.crt https://0.0.0.0:3000
	$ openssl s_client -connect 0.0.0.0:3000 -CAfile root-ca.crt

# Rotate a config
Edit the site.conf file locally

	server {
    	listen                443 ssl;
    	server_name           localhost;
    	ssl_certificate       /run/secrets/site.crt;
    	ssl_certificate_key   /run/secrets/site.key;

    	location / {
    	    root   /usr/share/nginx/html;
    	    index  index.html index.htm index.php;
    	}
	}

Create a new Docker config using the new site.conf, called site-v2.conf

	$ docker config create site-v2.conf site.conf

Update the nginx service to use the new config instead of the old one

	$ docker service update \
	  --config-rm site.conf \
	  --config-add source=site-v2.conf,target=/etc/nginx/conf.d/site.conf \
	  nginx

Verify that the nginx service is fully re-deployed

	$ docker config rm site.conf

To clean up, you can remove the nginx service, as well as the secrets and configs

	$ docker service rm nginx
	$ docker secret rm site.crt site.key
	$ docker config rm site-v2.conf
