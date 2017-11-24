#!/bin/bash

echo "文件访问控制ACL"
chmod 600 /etc/services
chmod 600 /etc/security/sepermit.conf
chmod 600 /etc/security/console.handlers
chmod 600 /etc/security/namespace.conf
chmod 600 /etc/security/chroot.conf
chmod 600 /etc/security/group.conf
chmod 600 /etc/security/console.perms
chmod 600 /etc/security/pam_env.conf
chmod 600 /etc/security/access.conf
chmod 600 /etc/security/namespace.init
chmod 600 /etc/security/time.conf

chmod +x /etc/rc.d/rc.local

# logging history
echo "logging history"
cat >> /etc/profile << EOF
# logging history
if [ "\$BASH" ]; then
      PROMPT_COMMAND='history -a >(tee -a ~/.bash_history | logger -p local3.notice -t "\$USER[\$\$] \$SSH_CONNECTION")'
fi
EOF

source /etc/profile

#system update
yum -y update

