################################################################################
#
# This program is part of the VirtualIP Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""VirtualInterface

VirtualInterface maps the interface and ip tables to interface objects

$Id: VirtualInterfaceMap.py,v 1.1 2010/08/10 18:12:57 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

import re
from Products.DataCollector.plugins.zenoss.snmp.InterfaceMap import InterfaceMap

class VirtualInterfaceMap(InterfaceMap):

    deviceProperties = \
        InterfaceMap.deviceProperties + ('zInterfaceMapIgnoreIpAddresses',)

    def process(self, device, results, log):
        """collect snmp information from this device"""
        getdata, tabledata = results
        rm = self.relMap()
        dontCollectIpAddresses = getattr(device, 'zInterfaceMapIgnoreIpAddresses', None)
        if (dontCollectIpAddresses 
            and re.search(dontCollectIpAddresses, device.manageIp)):
	    om = self.objectMap()
	    om.id = self.prepId("Virtual IP Address")
	    om.title = om.id
	    om.interfaceName = om.id
	    om.type = "softwareLoopback"
	    om.speed = 1000000000
	    om.mtu = 1500
	    om.ifindex = "1"
	    om.adminStatus = 1
	    om.operStatus = 1
	    om.monitor = False
            om.setIpAddresses = [device.manageIp, ]
	    rm.append(om)
	else:
            for om in super(VirtualInterfaceMap, self).process(device, results, log):
                newIpAddresses = []
                for ip in om.setIpAddresses:
                    if (dontCollectIpAddresses 
                        and re.search(dontCollectIpAddresses, ip.split('/')[0])):
                        continue
                    newIpAddresses.append(ip)
                om.setIpAddresses = newIpAddresses
	        rm.append(om)
        return rm
