################################################################################
#
# This program is part of the NWMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Interface2IP

Interface2IPMap maps the interface and ip tables to interface objects

$Id: Interface2IPMap.py,v 1.0 2009/02/09 16:37:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.zenoss.snmp.InterfaceMap import InterfaceMap

class Interface2IPMap(InterfaceMap):

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
	rm = self.relMap()
	om = self.objectMap()
	om.id = "Novell Second IP Address"
	om.title = om.id
	om.interfaceName = om.id
	om.id = self.prepId(om.interfaceName)
	om.type = "softwareLoopback"
	om.speed = 1000000000
	om.mtu = 1500
	om.ifindex = "1"
	om.adminStatus = 1
	om.operStatus = 1
	om.monitor = False
        om.setIpAddresses = [device.manageIp, ]
	rm.append(om)
        return rm


