#!/bin/bash

oidnum=$(snmpwalk -v1 -c $2 $1 .1.3.6.1.2.1.25.2.3.1.2 2>/dev/null | grep hrStorageRam | cut -d '.' -f 2 | cut -d ' ' -f 1)

usage=$(snmpwalk -v1 -c $2 $1 .1.3.6.1.2.1.25.2.3.1.6.$oidnum 2>/dev/null | cut -d ' ' -f 4)

total=$(snmpwalk -v1 -c $2 $1 .1.3.6.1.2.1.25.2.3.1.5.$oidnum 2>/dev/null | cut -d ' ' -f 4)

units=$(snmpwalk -v1 -c $2 $1 .1.3.6.1.2.1.25.2.3.1.4.$oidnum 2>/dev/null | cut -d ' ' -f 4)

if [ -n "$usage" ]
then
        percent=$(echo "($usage / $total * 100)" | bc -l 2>/dev/null | xargs printf "%1.0f")
        total=$(echo "($total * $units / 1.024)" | bc -l 2>/dev/null | xargs printf "%1.0f")
        usage=$(echo "($usage * $units / 1.024)" | bc -l 2>/dev/null | xargs printf "%1.0f")

        echo "OK|MemoryTotal=$total MemoryUsed=$usage PercentMemoryUsed=$percent"

else
        echo "Unknown"
fi
