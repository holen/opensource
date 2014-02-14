host { 'peer':
    ip => '192.168.1.121',
    host_aliases => [ "foo", "bar" ],
    ensure => 'present',
}
