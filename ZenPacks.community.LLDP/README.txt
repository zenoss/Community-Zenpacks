===========
LLDP Zenpack for Zenoss
===========

tested with Zenoss 3.0.1 and Zenoss 3.0.2



Overview
===========

This Zenpack will model switches that implement Local Link Discovery (LLDP) SNMP
mibs (.1.0.8802.1.1.2.1.3.7.1)

The collected data is available as seperate component on the Device page.

During Display, the pack will try to generate the correct links.
LocalInterface is trivial. For the remoteDevice it will search the Managment
IP of the remote System in Zenoss and create a link to the device owning it.
If this is not available it will display the textual name that LLDP-SNMP
provided. Same goes for the remote Interface


Known Issues
===========

The Details Page for an LLDPLink will always display links for RemoteSystem and 
RemoteInterface. If the Remote System is not monitored by zenoss those links
are broken.
I assume that this is a bug somewhere in zenoss javascript. The Grid renders
fine, only the details page is broken.


