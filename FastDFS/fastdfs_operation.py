#!/usr/bin/python

import subprocess, shlex
from os.path import basename
from fdfs_client.client import *
from fdfs_client.exceptions import *
from fdfs_client.connection import *

# upload file 
upload_file="/etc/iproute2/rt_tables"
client = Fdfs_client('/etc/fdfs/client.conf')
ret = client.upload_by_filename(upload_file)
remote_file_id = ret['Remote file_id']
print upload_file + ' --> ' + remote_file_id
print ret

# list upload file info
args = shlex.split("curl -I http://10.0.140.58:8090/%s"  %(remote_file_id))
print args
p = subprocess.Popen(args,stdout=subprocess.PIPE)
out = p.stdout.readlines()
for line in out:
    print line.strip()

# download file
downloadinfo = client.download_to_file(basename(upload_file), remote_file_id)
print downloadinfo

# del file
delinfo = client.delete_file(remote_file_id)	
print delinfo
