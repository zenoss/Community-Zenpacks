This zenpack will do the following:
------------------------------------

- Create a device class: /Devices/Server/ESX
- Apply a new FileSystem template to that class
- Add a libexec command to collect for the FileSystem template
- Add a new cmd collector plugin (VmwareEsxDf) and will be applied to the
  device class
- Add all ESX related MIBS 

So you can get all the VMFS filesystems of the esx server


Actions to take to get this zenpack to work:
----------------------------------------------

Add the esx server to zenoss
once it is added please fill in the:
  - zCommandPassword
  - zCommandUsername

The VmwareEsxDf will model the filesystem using ssh
but for the performance I will use snmp.
(I don't want to ssh every 5 min to the ESX server)

so on the esx server edit the /etc/snmp/snmpd.conf and add:
   exec .1.3.6.1.4.1.6876.99999.1 vdf /usr/sbin/vdf

The OID .1.3.6.1.4.1.6876.99999.1 is used by the FileSystem template
now restart the snmpd service on the ESX server:
   /etc/init.d/snmpd restart 

Now you are ready to remodel the device and the VMFS filesystems will be added
and after a few zencommand cycles you also will have the performance graphs
for the filesystem.

What needs to be done?
------------------------

If someone is good eneugh at python it would be nice that:
FileSystem template and VmwareEsxDf uses the 1.3.6.1.4.1.6876.99999.1 OID to
get what they want.


