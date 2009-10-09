#!/bin/sh

#nbclimagelist <netbackupclient/server host> <clientname> <netbackup policy> [netbackup server]
#netbackupclient/server host - host dedicated to running nbclimagelist commands through
#clientname - host to check for imagelists for
#netbackup policy - policy string to grep for
#netbackupserver - netbackup server to query clients againts

NBHOST=$1
NBCLIENT=$2
NBCLIENT='-client '`echo ${NBCLIENT%%.*}`
COMMAND=''
NBPOLICY=$3
NBSERVER=''
if [ -z $4 -a $4 != '' ]; then
        NBSERVER='-server '$4
fi
DATE='-s '`date -d yesterday +%m/%d/%Y`
COMMAND="/usr/openv/netbackup/bin/bpclimagelist ${NBSERVER} ${NBCLIENT} ${DATE}|grep ${NBPOLICY}"

#echo $COMMAND

output=`ssh root@${NBHOST} ${COMMAND}`
output_return=$?
results=''

#make sure ssh executed successfully
if [ ${output_return} -ne 0 ]; then
        results=${results}"NBCLIMAGELIST Critical|"
        echo -ne ${results}
        exit 1
else
        results=${results}"NBCLIMAGELIST OK|"
fi

#echo $output
#parse output into the following format:
#KB=<kb>KB FILES=<files>
KB=`echo ${output}|awk  '{print $5}'`
FILES=`echo ${output}|awk '{print $4}'`

results=${results}"KB=${KB}KB FILES=${FILES}|"
echo -ne ${results}

