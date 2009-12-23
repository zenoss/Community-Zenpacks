/usr/sbin/asterisk -rx "core show channels" | grep active | awk '{ print $1 }' | tr '\n' ' ' |awk '{ print var1 $1 var2 $2}' var1="active_channel:" var2=" active_calls:"
