#!/bin/bash
#####################################################################
# Author:		Jane Curry
# Date			March 7th, 2011
# Shellscript to count number of entries in IpSec jnxJsSrcNatStatsTable table
#
# Expects 	$1 = IP address
#		$2 = snmpVer
#		$3 = snmpCommunity
# Just get the poolType value - .4
# Output is in "Nagios plugin" format - string | var=value
#
#####################################################################
#set -x
count=0
for i in `/usr/bin/snmpwalk -$2 -c $3 $1 .1.3.6.1.4.1.2636.3.39.1.7.1.1.4.1.4 | cut -f1 -d ' '`
do
  count=$(($count+1))
done

if [ $count -eq 0 ]
then
  echo "IPSec NAT table count failed - status WARNING "
  exitStatus=1
else
  echo "IPSec NAT table count - status OK | ipSecNATCount=$count"
  exitStatus=0
fi
exit $exitStatus
 
