################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap

class DellEqualLogicHardDiskMap(SnmpPlugin):
    maptype = "DellEqualLogicHardDiskMap"
    modname = "ZenPacks.community.DellEqualLogicMon.DellEqualLogicHardDisk"
    relname = "harddisks"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('arrayDiskTable',
                    '.1.3.6.1.4.1.12740.3.1.1.1',
                    {
                        '.8': 'status',
                        '.3': '_model',
                        '.5': 'serialNumber',
                        '.4': 'FWRev',
                        '.6': '_sizeM',
                        '.11': 'bay',
                        '.12': 'diskType',
                    }
        ),
    )

    diskTypes = {0: 'Unknown',
                1: 'SATA',
                2: 'SAS',
                3: 'SATA-SSD',
                4: 'SAS-SSD',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        disktable = tabledata.get('arrayDiskTable')
        if not disktable: return
        rm = self.relMap()
        for oid, disk in disktable.iteritems():

            try:
                om = self.objectMap(disk)
		om.snmpindex = oid.strip('.')
                om.id = self.prepId("Disk %s" % (getattr(om, 'bay', 0)))
                om.description = "%s" % (getattr(om, '_model', 'hard disk'))
                om.setProductKey = om.description
                om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1), '%s (%d)' %(self.diskTypes[1], om.diskType))
                om.size = "%d" % (getattr(om, '_sizeM', 0) * 1048576)
            except AttributeError:
                continue
            rm.append(om)
        return rm
