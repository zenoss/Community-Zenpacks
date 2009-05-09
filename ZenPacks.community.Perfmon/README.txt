This Zenpack remotely pulls performance counter data from Windows Performance Monitor.

This can be used as an alternative to using SNMP-Informant and WMI.  The main reason to create this Zenpack was because the Exchange 2007 performance counters are not exposed to WMI.

To get the counters the Zenpack runs a perl script that uses "winexe" to remotely run the "typeperf" command on Windows Servers. The results from the typeperf command are sent back into Zenoss.

Included in the Zenpack are some sample counters that can be used as examples:

  Exchange Users
  Exchange Maximum Users
  Exchange Active Users
  CPU processor time

To get the syntax for the counters open up Performance Monitor under windows and search for the counter you want to use.  The format should be "\Performance Object\Performance Counter". 

The syntax for the perfmon script is:

perfmon.pl NUMBER_OF_COUNTERS HOSTNAME USERNAME PASSWORD COUNTER1 DATAPOINT1 COUNTER2...

  NUMBER_OF_COUNTERS : The number of counters for the script to retrieve. 
  HOSTNAME : The ip address or server hostname.
  USERNAME : The username and password for the server.  This comes from zWinUser.
  PASSWORD : Password for the username. This comes from zWinPassword.
  COUNTER1 : The Counter name to retrieve performance data from.  
  DATAPOINT1 : The Datapoint name under Zenoss to store the counter data.
  Additional Counters and Datapoints as required.  There should always be both a datapoint and counter.

