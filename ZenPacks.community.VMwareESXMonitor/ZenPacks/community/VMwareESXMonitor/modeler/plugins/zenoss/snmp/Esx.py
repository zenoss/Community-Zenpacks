###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
__doc__="""Esx
Plugin to gather information about virtual machines running
under a VMWare ESX server v3.0
"""

import Globals
from Products.DataCollector.plugins.CollectorPlugin \
     import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps \
     import ObjectMap

class Esx(SnmpPlugin):

    # compname = "os"
    relname = "guestDevices"
    modname = 'ZenPacks.zenoss.ZenossVirtualHostMonitor.VirtualMachine'
    
    columns = {
         '.1': 'snmpindex',
         '.2': 'displayName',
         '.4': 'osType',
         '.5': 'memory',
         '.6': 'adminStatus',
         '.7': 'vmid',
         '.8': 'operStatus',
         }

    snmpGetTableMaps = (
        GetTableMap('vminfo', '.1.3.6.1.4.1.6876.2.1.1', columns),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        table = tabledata.get("vminfo")
        rm = self.relMap()
        for info in table.values():
            info['adminStatus'] = info['adminStatus'] == 'poweredOn'
            info['operStatus'] = info['operStatus'] == 'running'
            info['snmpindex'] = info['vmid']
            del info['vmid']
            om = self.objectMap(info)
            om.id = self.prepId(om.displayName)
            rm.append(om)
        return [rm]
