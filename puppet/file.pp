file {
	"/tmp/1.txt":
	source => "/tmp/file.pp",
	mode => 600,
	# content => "hello world",
    	# /var/lib/puppet/clientbucket/
    	backup => ".bak"
}
