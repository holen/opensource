#!/usr/bin/python

from fdfs_client.client import *
from fdfs_client.exceptions import *
from fdfs_client.connection import *

upload_file="/etc/iproute2/rt_tables"
client = Fdfs_client('/etc/fdfs/client.conf')
ret = client.upload_by_filename(upload_file)
print upload_file + ' --> ' + ret['Remote file_id']
print ret
