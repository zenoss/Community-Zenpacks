#!/bin/bash
####################
# Roman@Tikhonov.org
####################
#Sitronics
#2009
#

#export CONNECT_STRING="sys/sys@DB as sysdba"
export ORACLE_BASE=/opt/zenoss/oracle
export CONNECT_STRING=$1
if [ x$2 == x ]
	then export ORACLE_HOME=$ORACLE_BASE/client
	else export ORACLE_HOME=$2
fi
export ORACLE_SID=OMEGA #fake
export PATH=$ORACLE_HOME/bin:$PATH
#USAGE : COMMAND CONNECT_STRING oracle_home
sqlplus -s /nolog <<-EOF > /tmp/sql_out.temp

connect $CONNECT_STRING
set HEADING OFF
set PAGESIZE 0
set linesize 120
col metric_name format a40
col value format 999999990.9999
select metric_name||':' Parameter,value from SYS.V\$SYSMETRIC where metric_id in (2003,2004,2006,2016,2018,2057,2067,2071,2075,2098,2101,2102,2103,2107,2108,2114,2135) and group_id=2 order by Parameter;
EOF



sed -e 's/:\+\s\+/:/'  -e 's/ /_/g' -e '/^$/d' -e 's/[(%)]//g'  -e '/^1/d' -e 's/[(*)]// ' /tmp/sql_out.temp > /tmp/sql_out.temp.1

sed -ni 'H;${x;s/\n/ /g;p}' /tmp/sql_out.temp.1

cat /tmp/sql_out.temp.1
rm /tmp/sql_out.*
