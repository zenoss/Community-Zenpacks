#!/bin/bash

n=0
total=0

snmplines=$(snmpwalk -v1 -c $2 $1 1.3.6.1.2.1.25.3.3.1.2 2>/dev/null | wc -l)

if [ $snmplines != 0 ]
then
        snmpwalk -v1 -c $2 $1 1.3.6.1.2.1.25.3.3.1.2 2>/dev/null | while read line
        do
                value=$(echo "$line" | cut -d ' ' -f 4)
                total=$(echo "($total + $value)" | bc -l 2>/dev/null | xargs printf "%1.0f")

                n=$(echo "($n + 1)" | bc)

                if [ $snmplines == 1 ]
                then
                        output="OK|CPU$n=$value Total=$total"
                        echo "$output"
                else
                        if [ $snmplines != $n ]
                        then
                                if [ $n == 1 ]
                                then
                                        output="OK|CPU$n=$value"
                                else
                                        output="$output CPU$n=$value"
                                fi
                        else
                                output="$output CPU$n=$value Total=$(echo "($total / $snmplines)" | bc -l 2>/dev/null | xargs printf "%1.0f")"
                                echo "$output"
                        fi
                fi
        done
else
        echo "Unknown"
fi
