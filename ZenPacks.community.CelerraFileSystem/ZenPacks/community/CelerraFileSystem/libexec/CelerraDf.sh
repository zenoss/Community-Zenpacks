#!/bin/bash
#  
# Celerra NAS FileSystem command
# 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# please add the following to your NAS in the /etc/snmp/snmpd.conf and restart the snmpd deamon
#  exec .1.3.6.1.4.1.1139.99999.1 server_df /nas/bin/server_df
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# Call this command as follows:
# CelerraDf.sh [devicename] [snmp read community] [mount point] 
#
# For complete information please visit: http://www.zenoss.com/oss/
#
# Created By  :  Wouter D'Haeseleer
# Created On  :  05-11-2007
# Company     :  Imas NV
#
#
# Re-Edited By: Randy Schneiderman
# Re-Edited On: 07/21/2008
# Comapany:     Stroz Friedberg
#
# New Comments: Based on the VMwareESX ZenPack, this script uses the same code
#               with the exception of the OID being used and the variable name.
#               This has been successfully tested with EMC's Celerra Network
#               Server v5.5.
#
###########################################################################

device=$1
community=$2
mount=$3

# execute the command on server_df command on the esx server
server_df=`snmpwalk -v2c -c $community $device 1.3.6.1.4.1.1139.99999.1.101`

#Remove all unwanted data
server_df=`echo "$server_df" | sed 's/"//g;s/SNMPv2-SMI::enterprises.1139.99999.1.101.* = STRING: //g'`

#Do a grep for the correct filesystem
#server_df=`echo "$server_df" |  grep -e $mount$ -e Filesystem
server_df=`echo "$server_df" |  grep -e $mount$`

# Parse the Datapoints
usedBlocks=`echo "$server_df" | awk '{ print $3 }'`
availBlocks=`echo "$server_df" | awk '{ print $4 }'`
totalBlocks=`echo "$server_df" | awk '{ print $2 }'`

# give the result
echo "DISK OK | usedBlocks=$usedBlocks availBlocks=$availBlocks totalBlocks=$totalBlocks"
