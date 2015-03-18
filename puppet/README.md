# Install puppet on ubuntu12.04
Download release deb

    wget https://apt.puppetlabs.com/puppetlabs-release-wheezy.deb

Install deb    

    dpkg -i puppetlabs-release-wheezy.deb

Update apt
    
    apt-get Update

Version 3.4.2

##A test

Master

    apt-get install puppetmaster
    /etc/init.d/puppetmaster start
    vim /etc/hostname
	puppet-server.w.cn
    vim /etc/hosts
	agent.w.cn
    vim /etc/puppet/manifests/site.pp
	node default { file { "/tmp/puppettest1.txt": content => "Hello, First Puppet test"; } }
    puppet cert list
    puppet cert sign agent.w.cn
    puppet parser validate /etc/puppet/modules/test/manifests/init.pp
    puppet agent --test --noop --environment [development, testing, production]

agent 

    apt-get install puppet 
    /etc/init.d/puppet
    vim /etc/hostname
	agent.w.cn
    vim /etc/hosts
	puppet-server.w.cn
    puppet agent --server puppet-server.w.cn --test --noop
    puppet agent --server puppet-server.w.cn --test
    more /tmp/puppettest1.txt
    find /var/lib/puppet/ssl/ -iname 'hostname'.pem | xargs -I {} rm -rf {}

# Install foreman

    echo "deb http://deb.theforeman.org/ precise stable" > /etc/apt/sources.list.d/foreman.list
    wget -q http://deb.theforeman.org/foreman.asc -O- | apt-key add - 
    apt-get update && apt-get install foreman-installer
    apt-get install foreman foreman-mysql foreman-libvirt foreman-proxy
    foreman-installer -i
    /etc/init.d/foreman start
    /etc/init.d/foreman-proxy start
