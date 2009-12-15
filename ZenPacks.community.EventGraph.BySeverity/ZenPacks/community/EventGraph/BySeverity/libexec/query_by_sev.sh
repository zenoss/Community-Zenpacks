#!/bin/bash

while getopts "S:H:" opt; do
        case $opt in
        S) SEVERITY=$OPTARG;;
        H) DEVICE=$OPTARG;;
        * ) echo "Usage: query_by_sev.sh -H <device> -S <0-5>"; exit 1;;
	esac
done

if [ -z "$DEVICE" ]; then
   echo "Usage: query_by_sev.sh -H <device> -S <0-5>"; exit 1
elif [ -z "$SEVERITY" ]; then
   echo "Usage: query_by_sev.sh -H <device> -S <0-5>"; exit 1
fi

NOW=`date +%s`
START=`date --date "5 minutes ago" +%s`

COUNT=`mysql --skip-column-names -uzenoss -pzenoss events<<EOF
select (select count(*) from history where severity="$SEVERITY" and device="$DEVICE" and lastTime>"$START" and lastTime<"$NOW") +
(select count(*) from status where severity="$SEVERITY" and device="$DEVICE" and lastTime>"$START" and lastTime<"$NOW")
as total;
EOF`

echo "$DEVICE Severity | EventSev$SEVERITY=$COUNT"
