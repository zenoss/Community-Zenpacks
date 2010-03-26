#!/usr/bin/env python
"""
Simply connect to the Zenoss MySQL events table and query the last 5 minutes for a single device.  Spit out the results in a Nagios format.
"""

import sys
import subprocess

if (len(sys.argv) > 1):
  device = sys.argv[1]
else:
  print "You must specify the device."
  sys.exit(1)

severity = [0]*6
query = query = "SELECT severity, COUNT(severity) FROM history WHERE device=\\\""+device+"\\\" AND lastTime>(UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 5 MINUTE))) GROUP BY severity UNION ALL SELECT severity, COUNT(severity) FROM status WHERE device=\\\""+device+"\\\" AND lastTime>(UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 5 MINUTE))) GROUP BY severity;"
mysql = subprocess.Popen(['mysql -s -uzenoss -pzenoss events -e \"' + query +'\"'], shell=True, stdout=subprocess.PIPE)
"""
mysql output is like 
0	21
2	469
3	1
4	63
5	14
3	1
4	10
5	2
"""
result = mysql.stdout.read().split('\n')
#['3\t1', '4\t8', '5\t2', '']
for row in result:
  if (row):
    column = row.split()
    severity[int(column[0])] += int(column[1])

print device + "Events | EventSev0="+str(severity[0])+" EventSev1="+str(severity[1])+" EventSev2="+str(severity[2])+" EventSev3="+str(severity[3])+" EventSev4="+str(severity[4])+" EventSev5="+str(severity[5])
