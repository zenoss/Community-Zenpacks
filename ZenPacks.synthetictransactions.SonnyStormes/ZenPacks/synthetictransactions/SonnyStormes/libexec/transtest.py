#!/usr/bin/env python
#Author - Sonny Stormes
#This script will execute the twill script created by the user, time the execution of the synthetic transaction, and report back in standard Nagios output that can be easily parsed by Zenoss.

import sys, time, subprocess

url = sys.argv[1]
test = sys.argv[2]

t0 = time.time()
status = subprocess.call("twill-sh -q -u http://"+url+" "+test, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
final = time.time() - t0

if status == 0:
        print  "SYNTHETIC TRANSACTION SUCCESSFUL|time="'%4.2lf'%final+";;;0.00"
	sys.exit(0)
else:
        print  "SYNTHETIC TRANSACTION FAILED|time="'%4.2lf'%final+";;;0.00"
	sys.exit(2)
