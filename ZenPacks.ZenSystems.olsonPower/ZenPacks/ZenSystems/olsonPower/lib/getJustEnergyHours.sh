#!/bin/bash
###############################################################################################
# Author:		Jane Curry
# Date			March 10th 2011
# Revised:		
#
# Shellscript to use indidual snmpget commands to get energy from Olson power meters
#  We really want to get this value so snmpget has reties = 10 and timeout = 5 secs
# Note that all values are delivered as DisplayStrings so an SNMP template
#   cannot be used.
# host is first parameter; communty name is second parameter: version is third parameter
#
# Driven by olson_power command performance template
# ${here/ZenPackManager/packs/ZenPacks.ZenSystems.olsonPower/path}/lib/getJustEnergy.sh ${here/manageIp} ${here/zSnmpCommunity} ${here/zSnmpVer}
#
###############################################################################################
#set -x
# Get energy OID - comes in format          "1234567.9"
# so convert from string to integer with bc utility

energy_hours=$(/usr/bin/snmpget  -r 10 -t 5 -$3 -c $2  -O qvU  $1 1.3.6.1.4.1.17933.1.1.22 2>/dev/null)
energy_hours=$(echo $energy_hours | bc -l 2>/dev/null)

if [ -n "$energy_hours" ]
then
  echo "OK|energy_hours=$energy_hours"
else echo "Unknown"
fi

