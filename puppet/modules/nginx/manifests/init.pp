class nginx {

$nginx_conf_d = "/etc/nginx/conf.d"

    package { 'nginx':
	provider => apt,
	ensure => installed,
    }

    service { 'nginx':
	ensure => "running",
	enable => true,
	path => "/etc/init.d",
	hasrestart => true,
	hasstatus => true,
	subscribe => File["/etc/nginx/nginx.conf"],
    }

    file { 'nginx.conf':
	ensure => present,
	mode => 644, owner => root, group => root,
	path => '/etc/nginx/nginx.conf',
	content => template("nginx/nginx.conf.erb"),
	notify => Exec["reload-nginx"],
	require => Package["nginx"],
    }

    file { $nginx_conf_d:
	ensure => directory,
	recurse => true,
	purge => true,
	source => "puppet:///modules/nginx/conf.d",
	notify => Exec["reload-nginx"],
	require => Package["nginx"],
    }

    exec { 'reload-nginx':
	command => "/etc/init.d/nginx reload",
	refreshonly => true,
    }

}
