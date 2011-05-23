###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, 2009 Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__ = """OlsonNewDeviceMap
Try to determine OS and hardware manufacturer information based on
the SNMP description (sysDescr).
"""

import re

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap,RelationshipMap,  MultiArgs
from Products.DataCollector.EnterpriseOIDs import EnterpriseOIDs

class OlsonNewDeviceMap(SnmpPlugin):
    """
    Record basic hardware/software information based on the snmpDscr OID.
    Note that this doesn't work with Olson devices if .0 on end of OID
    """
    maptype = "OlsonNewDeviceMap" 

    snmpGetMap = GetMap({ 
             '.1.3.6.1.2.1.1.1' : 'snmpDescr',
             '.1.3.6.1.2.1.1.2' : 'snmpOid',
             '.1.3.6.1.2.1.1.5' : 'snmpSysName',
             '.1.3.6.1.4.1.17933.1.1.1' : 'setHWProductKey',
             '.1.3.6.1.4.1.17933.1.1.4' : '_macAddr',
             '.1.3.6.1.4.1.17933.1.1.6' : '_ipAddr',

             })

    osregex = (
        # Olson 9016-V01 PDU
        re.compile(r'^(Olson) (\S+) (\S+)'),                 # Olson
   
        #GENERIC unix
        re.compile(r'(\S+) \S+ (\S+)'),                 # unix
    )

    def olsonInterface(self, manageIp, macaddr):
        om = ObjectMap({}, compname = "os",
                        modname = "Products.ZenModel.IpInterface")
        om.id = self.prepId("eth0")
        om.title = om.id
        om.interfaceName = om.id
        om.description = "Manually Kludged"
        om.type = "manual"
        om.speed = 10000000
        om.mtu = 1500
        om.ifindex = "1"
        om.adminStatus = 1
        om.operStatus = 1
        om.monitor = False
        om.setIpAddresses = [manageIp, ]
        om.macaddress = macaddr
#        om.lockFromDeletion()
#        om.lockFromUpdates()
        return RelationshipMap(relname = "interfaces", compname = "os",
                               modname = "Products.ZenModel.IpInterface",
                               objmaps = [om,])

    def process(self, device, results, log):
        """
        Collect SNMP information from this device
        """
        log.info('Processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not getdata:
            log.warn("Unable to retrieve getdata from %s", device.id)
            log.warn("Does snmpwalk -v1 -c community %s 1.3.6.1.2.1.1 work?", 
                     device.id)
            return
        log.debug("%s getdata = %s", device.id, getdata)
        maps = []
        om = self.objectMap(getdata)
        
        if om.snmpDescr:
            descr = re.sub("\s", " ", om.snmpDescr)
            for regex in self.osregex:
                m = regex.search(descr)
                if m: 
                    groups = m.groups()
                    if groups[0] == 'Olson':
                        om.setOSProductKey = MultiArgs(" ".join(groups[0:3])
                                                     , 'Olson')
                    else:
                        om.setOSProductKey = " ".join(groups)
                    log.debug("OSProductKey=%s", om.setOSProductKey)
                    break
        maps.append(om)
        if device.manageIp:
            maps.append(self.olsonInterface(om._ipAddr, om._macAddr))
        return maps
