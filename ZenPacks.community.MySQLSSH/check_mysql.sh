#!/bin/bash

#arg 1 is ${here/zMySqlUsername}
#arg 2 is ${here/zMySqlPassword}

output1=$(mysql -s -u$1 -p$2 -e 'SHOW GLOBAL STATUS'|tr '\t' '=')
rc=$?

echo $rc\|$output1
exit $rc

