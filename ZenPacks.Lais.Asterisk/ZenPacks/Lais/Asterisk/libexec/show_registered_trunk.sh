/usr/sbin/asterisk -rx "sip show registry" | sed -e '1d' | wc -l |  awk '{print var1 $1}' var1="registered_trunk:"
