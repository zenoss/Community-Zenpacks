#!/bin/bash
#  
# VMware ESX FileSystem command
# 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# please add the following to your ESX server in the /etc/snmp/snmpd.conf and restart the snmpd deamon
#  exec .1.3.6.1.4.1.6876.99999.1 vdf /usr/sbin/vdf
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# Call this command as follows:
# vmware-esx.sh [devicename] [snmp read community] [mount point] 
#
# Created on: 16nov2007 by Wouter D'Haeseleer

device=$1
community=$2
mount=$3

# execute the command on vdf command on the esx server
vdf=`snmpwalk -v1 -c $community $device .1.3.6.1.4.1.6876.99999.1.101`

#Remove all unwanted data
vdf=`echo "$vdf" | sed 's/"//g;s/SNMPv2-SMI::enterprises.6876.99999.1.101.. = STRING: //g'`

#Do a grep for the correct filesystem
#vdf=`echo "$vdf" |  grep -e $mount$ -e Filesystem
vdf=`echo "$vdf" |  grep -e $mount$`

# Parse the Datapoints
usedBlocks=`echo "$vdf" | awk '{ print $3 }'`
availBlocks=`echo "$vdf" | awk '{ print $4 }'`
totalBlocks=`echo "$vdf" | awk '{ print $2 }'`

# give the result
echo "DISK OK | usedBlocks=$usedBlocks availBlocks=$availBlocks totalBlocks=$totalBlocks"
