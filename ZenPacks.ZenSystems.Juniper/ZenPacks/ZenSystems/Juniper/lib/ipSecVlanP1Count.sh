#!/bin/bash
#####################################################################
# Author:		Jane Curry
# Date			March 4th, 2011
# Shellscript to count number of entries in IpSec VPN Phase 1 table
#
# Expects 	$1 = IP address
#		$2 = snmpVer
#		$3 = snmpCommunity
# Output is in "Nagios plugin" format - string | var=value
#
#####################################################################
#set -x
count=0
for i in `/usr/bin/snmpwalk -$2 -c $3 $1 .1.3.6.1.4.1.2636.3.52.1.1.2.1.6 | cut -f1 -d ' '`
do
  count=$(($count+1))
done

if [ $count -eq 0 ]
then
  echo "IPSec VPN Phase 1 table count failed - status WARNING "
  exitStatus=1
else
  echo "IPSec VPN Phase 1 table count - status OK | ipSecVPNP1Count=$count"
  exitStatus=0
fi
exit $exitStatus
 
