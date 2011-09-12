#!/bin/bash
###############################################################################################
# Author:		Jane Curry
# Date			Jan 26th 2011
# Revised:		
#
# Shellscript to use indidual snmpget commands to get
#    voltage, current, power, energy and temperature from Olson power meters
# Note that all values are delivered as DisplayStrings so an SNMP template
#   cannot be used.
# host is first parameter; communty name is second parameter: version is third parameter
#
# Driven by olson_power command performance template
# ${here/ZenPackManager/packs/ZenPacks.ZenSystems.olsonPower/path}/lib/getPowerValues.sh ${here/manageIp} ${here/zSnmpCommunity} ${here/zSnmpVer}
#
###############################################################################################
#set -x
# Get voltage OID - comes in format          "232.5"
# so convert from string to integer with bc utility

volts=$(/usr/bin/snmpget -$3 -c $2  -O qvU  $1 1.3.6.1.4.1.17933.1.1.19 2>/dev/null)
volts=$(echo $volts | bc -l 2>/dev/null)

amps=$(/usr/bin/snmpget -$3 -c $2  -O qvU  $1 1.3.6.1.4.1.17933.1.1.20 2>/dev/null)
amps=$(echo $amps | bc -l 2>/dev/null)

power=$(/usr/bin/snmpget -$3 -c $2  -O qvU  $1 1.3.6.1.4.1.17933.1.1.21 2>/dev/null)
power=$(echo $power | bc -l 2>/dev/null)

energy=$(/usr/bin/snmpget -$3 -c $2  -O qvU  $1 1.3.6.1.4.1.17933.1.1.22 2>/dev/null)
energy=$(echo $energy | bc -l 2>/dev/null)

temp=$(/usr/bin/snmpget -$3 -c $2  -O qvU  $1 1.3.6.1.4.1.17933.1.1.24 2>/dev/null)
temp=$(echo $temp | bc -l 2>/dev/null)

if [ -n "$volts" ]
then
  echo "OK|voltage=$volts  current=$amps power=$power energy=$energy temp=$temp"
else echo "Unknown"
fi

