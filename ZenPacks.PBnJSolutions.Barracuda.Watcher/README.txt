This ZenPack consists of an rrd template called Barracuda which defined at
/Devices/Network.  You'll want to bind it to your Barracuda device which
presumably sits somewhere below that point.

The template contains performance graphs for the inbound queue and the number
of:
	allowed
	tagged
	quarantined
	virus
	bad recipient
	spam
messages received by the Barracuda.

In addition, it has a threshold for the inbound queue size of 25 but that may
need tweaking.

All this information is gathered from the Barracuda device by retrieving the
contents of the stats.cgi page over an https connection with the "wget"
utility.  The output of this http GET command is an XML document which is then
parsed by some PERL code called "check_cuda" which is provided as a datasource
inside this ZenPack / template.  The nice thing here is that by not using
SNMP, this ZenPack will work for collecting data on even the 300 series
