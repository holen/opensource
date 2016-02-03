# supervisor 
supervisord -- run a set of applications as daemons

Install

	apt-get install supervisor

configure

	echo_supervisord_conf > /etc/supervisor/supervisord.conf
	
run 

	/usr/bin/python /usr/bin/supervisord -c /tmp/supervisord.conf

