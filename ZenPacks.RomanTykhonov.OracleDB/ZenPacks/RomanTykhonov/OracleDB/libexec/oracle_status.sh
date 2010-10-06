#!/bin/bash
####################
# Roman@Tikhonov.org
####################
#

#export CONNECT_STRING="sys/sys@DB as sysdba"
#export ORACLE_BASE=/opt/oracle
export CONNECT_STRING=$1
if [ x$2 == x ]
	then echo First Parameter is connection string to DB and Second parameter have to be ORACLE_HOME variable && exit 1
	else export ORACLE_HOME=$2
fi
export ORACLE_SID=OMEGA #fake
export PATH=$ORACLE_HOME/bin:$PATH
RAND=$$
#USAGE : COMMAND CONNECT_STRING oracle_home
sqlplus -s /nolog <<-EOF > /tmp/${RAND}.sql_out.temp

connect $CONNECT_STRING
set HEADING OFF
set PAGESIZE 0
set linesize 120
col metric_name format a40
col value format 999999990.9999
select metric_name||':' Parameter,value from V\$SYSMETRIC where metric_id in (2003,2004,2006,2016,2018,2057,2067,2071,2075,2098,2101,2102,2103,2107,2108,2114,2135) and group_id=2 order by Parameter;
EOF



sed -e 's/:\+\s\+/:/'  -e 's/ /_/g' -e '/^$/d' -e 's/[(%)]//g'  -e '/^1/d' -e 's/[(*)]// ' /tmp/${RAND}.sql_out.temp > /tmp/${RAND}.sql_out.temp.1

sed -ni 'H;${x;s/\n/ /g;p}' /tmp/${RAND}.sql_out.temp.1

cat /tmp/${RAND}.sql_out.temp.1
rm /tmp/${RAND}.sql_out.*
