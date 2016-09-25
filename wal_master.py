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
mqry = 'select * from pg_current_xlog_location();'
db = 'vagrantdb'




c = StatsdClient('localhost', 8125)


#define methods that will remove "/" on the value
def rem(wal):
  return re.sub("/", "", wal)

#remove extra line #print mwal.rstrip('\n')

try:
  while True:
    # get the wal status on master and slave
    mwal = subprocess.check_output(['psql', '-q', '-t', '-A', '-w', '-c', mqry, '-d', db])
    #then convert to integer as a "bytes" value
    mas = rem(mwal)
    master = int(mas, 16)

    c.incr('wal_master_status', master)
    print master
    #print slave
    time.sleep(7)

except KeyboardInterrupt:
  print "Exit Status"
