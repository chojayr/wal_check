#!/usr/local/bin/python2.7
import socket
import sys
import time
import re
import os
from statsd import StatsdClient
from subprocess import Popen, PIPE
import subprocess

masterip = sys.argv[1]
sqry = 'select * from pg_last_xlog_replay_location();'
#define databse
db = 'vagrantdb'

c = StatsdClient('localhost', 8125)

#define methods that will remove "/" on the value
def rem(wal):
  return re.sub("/", "", wal)

#remove extra line #print mwal.rstrip('\n')

try:
  while True:
    # get the wal status on master and slave
    swal = subprocess.check_output(['psql', '-q', '-t', '-A', '-w', '-c', sqry, '-d', db])
    #then convert to integer as a "bytes" value
    sla = rem(swal)
    slave = int(sla, 16)

    #lagval = master - slave
    c.incr('wal_slave_status', slave)
    print slave
    time.sleep(7)

except KeyboardInterrupt:
  print "Exit Status"
