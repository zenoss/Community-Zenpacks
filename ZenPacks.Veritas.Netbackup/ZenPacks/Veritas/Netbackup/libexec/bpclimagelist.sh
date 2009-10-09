#!/bin/sh

#$ZENCOMMAND may need to be modified to suite your zenoss environment
#this should point to the common/bin directory within zenoss
ZENCOMMAND=$ZENHOME/common/bin/winexe


#bpclimagelist <netbackupclient/server host> <username> <password> <clientname> <netbackup policy> [netbackup server]
#netbackupclient/server host - host dedicated to running nbclimagelist commands through
#clientname - host to check for imagelists for
#netbackup policy - policy string to grep for
#netbackupserver - netbackup server to query clients againts

NBHOST=$1
NBHOSTUSERNAME=$2
NBHOSTUSERNAMEPASSWORD=$3
NBCLIENT=$4
NBCLIENT='-client '`echo ${NBCLIENT%%.*}`
NBPOLICY=$5
NBSERVER=''
#if [ -z $6 -o ${6} != '' ]; then
#        NBSERVER='-server '$6
#fi
DATE='-s '`date -d yesterday +%m/%d/%Y`
NBPATH='"c:\Program Files\Veritas\NetBackup\bin\bpclimagelist.exe"'
COMMAND=''
COMMAND="${NBPATH} ${NBSERVER} ${NBCLIENT} ${DATE}"

#echo $COMMAND

output=`${ZENCOMMAND} -U "${NBHOSTUSERNAME}%${NBHOSTUSERNAMEPASSWORD}" //${NBHOST} "${COMMAND}" | grep ${NBPOLICY}`
output_return=$?
results=''
#echo '$output_return='$output_return
#echo '$output='$output

#make sure ssh executed successfully
if [ ${output_return} -ne 0 ]; then
        results=${results}"NBCLIMAGELIST Critical|${output}"
        echo -ne ${results}
        exit 1
else
        results=${results}"NBCLIMAGELIST OK|"
fi

#echo '$output='$output

#parse output into the following format:
#KB=<kb>KB FILES=<files>
KB=`echo ${output}|awk  '{print $5}'`
FILES=`echo ${output}|awk '{print $4}'`

results=${results}"KB=${KB}KB FILES=${FILES}|"
echo -ne ${results}
