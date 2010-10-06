#!/bin/bash
####################
# Roman@Tikhonov.org
####################
#
if [ x$2 == x ]
        then echo First Parameter is ORACLE_SID and Second parameter have to be ORACLE_HOME variable && exit 1
        else export ORACLE_HOME=$2
fi
export ORACLE_SID=XE #fake
export PATH=$PATH:$ORACLE_HOME/bin


$ORACLE_HOME/bin/tnsping $1 10|tail -10 |awk -F " " 'BEGIN{MAX=0;MIN=0;i=0;SUM=0;ERROR=0} {if ($1=="OK") {ms=split($(NF-1),array,"\x28");i++;array2[i]=array[2]; } else {ERROR++}} END{for (i=1;i<=10;i++) {if (array2[i]<MIN){MIN=array2[i]}; if (array2[i]>MAX){MAX=array2[i]};SUM=array2[i]+SUM};   print "AVER:" SUM/10 " MAX:" MAX " MIN:" MIN " ERROR:" ERROR}'

