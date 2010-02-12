#!/bin/bash
####################
# Roman@Tikhonov.org
####################
#Sitronics
#2009
#


export CONNECT_STRING=$1
#export CONNECT_STRING="sys/sys@DB as sysdba"
export ORACLE_BASE=/opt/zenoss/oracle
if [ x$2 == x ]
       then export ORACLE_HOME=$ORACLE_BASE/client
       else export ORACLE_HOME=$2
fi
export ORACLE_SID=OMEGA #fake
export PATH=$ORACLE_HOME/bin:$PATH

#USAGE : COMMAND CONNECT_STRING

sqlplus -s /nolog <<-EOF > /tmp/sql_add.temp

connect $CONNECT_STRING
set HEADING OFF
set PAGESIZE 0
set linesize 120

SELECT 'ListenerIsOut:0' FROM DUAL
;

select session_type||':'||to_char(sum(active_sess)+sum(inactive_sess))||' '||session_type||'Active:'||to_char(sum(active_sess))||
' '||session_type||'Inactive:'||to_char(sum(inactive_sess)) "fignya"
from (
select case when sess.username is null then 'BackgroundProcesses'
            when sess.username in ('SYSTEM', 'SYSMAN', 'SYS', 'DBSNMP') then 'SystemUsers'
            else 'UserProcesses'
       end as session_type,
       decode(status, 'ACTIVE', 1, 0) active_sess,
       decode(status, 'INACTIVE', 1, 0) inactive_sess
from v\$session sess)
group by session_type
order by session_type;

SELECT
    'TBS-'|| d.tablespace_name || '-FILE_ID-' ||d.file_id || '-Used_Percent:' ||  TRUNC(((NVL((d.bytes - s.bytes) , d.bytes)) / d.bytes) * 100)
FROM
    sys.dba_data_files d
  , v\$datafile v
  , ( select file_id, SUM(bytes) bytes
      from sys.dba_free_space
      GROUP BY file_id) s
WHERE
      (s.file_id (+)= d.file_id)
  AND (d.file_name = v.name)
UNION
SELECT
    'TBS-' || dd.tablespace_name || '-FILE_ID-'   ||dd.file_id || '-Used_Percent:' || TRUNC((nvl(t.bytes_cached, 1) / dd.bytes) * 100)
FROM
    sys.dba_temp_files dd
    join v\$tempfile v on dd.file_id = v.file#
    left join v\$temp_extent_pool t on t.file_id = dd.file_id
;

SELECT
    'ASM-' || name || '-Percent_Used:' || ROUND((1- (free_mb / total_mb))*100, 2)
FROM
    v\$asm_diskgroup ORDER BY name
;

SELECT 'BlockingSessions:'||count (*) --gvh.SID sessid, gvs.serial# serial,
                 -- gvh.inst_id instance_id
               FROM gv\$lock gvh, gv\$lock gvw, gv\$session gvs
              WHERE (gvh.id1, gvh.id2) IN (SELECT id1, id2
                                             FROM gv\$lock
                                            WHERE request = 0
                                           INTERSECT
                                           SELECT id1, id2
                                             FROM gv\$lock
                                            WHERE lmode = 0)
                AND gvh.id1 = gvw.id1
                AND gvh.id2 = gvw.id2
                AND gvh.request = 0
                AND gvw.lmode = 0
                AND gvh.SID = gvs.SID
                AND gvh.inst_id = gvs.inst_id
;


SELECT 'Flash_volume-' || name || '-UsedPercent:' || ROUND((space_used / space_limit)*100, 2) || ' FlashReclaimableSpacePercent:' || ROUND((space_reclaimable / space_limit)*100, 2)
FROM
    v\$recovery_file_dest
ORDER BY name
;


SELECT 'DbaInvalidObjects:'|| count(*)  
FROM dba_objects
WHERE status <> 'VALID'
ORDER BY owner, object_name
;
EOF



sed -e '/^$/d' -e '/^[123456789]/d' -e 's/+/ASMVOLUME-/g'  -e 's/\//-/g' -e 's/--/-/g' -e 's/ORA-12541:/ListenerIsOut:1 / ' /tmp/sql_add.temp > /tmp/sql_add.temp.1
sed -ni 'H;${x;s/\n/ /g;p}' /tmp/sql_add.temp.1

cat /tmp/sql_add.temp.1
rm  /tmp/sql_add.*
