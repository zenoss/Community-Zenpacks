################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellLogicalDiskMap

DellLogicalDiskMap maps the cpqDaLogDrvTable, cpqFcaLogDrvTable or cpqScsiLogDrvTabletables
to disks objects

$Id: DellHardDiskMap.py,v 1.1 2010/02/19 20:05:19 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap

class DellLogicalDiskMap(SnmpPlugin):
    """Map Dell System Management Logical Disk table to model."""

    maptype = "LogicalDiskMap"
    modname = "ZenPacks.community.DellMon.DellLogicalDisk"
    relname = "logicaldisks"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('virtualDiskTable',
                    '1.3.6.1.4.1.674.10893.1.20.140.1.1',
                    {
                        '.2': 'id',
                        '.3': 'description',
                        '.4': 'status',
                        '.6': '_sizeM',
                        '.7': 'size',
                        '.13': 'diskType',
                        '.14': '_stripesizeM',
                        '.15': 'stripesize',
                    }
        ),
    )

    diskTypes = {1: 'Concatenated',
                2: 'RAID0',
                3: 'RAID1',
                4: 'RAID2',
                5: 'RAID3',
                6: 'RAID4',
                7: 'RAID5',
                8: 'RAID6',
                9: 'RAID7',
                10: 'RAID10',
                11: 'RAID30',
                12: 'RAID50',
                13: 'Add Spares',
                14: 'Delete Logical',
                15: 'Transform Logical',
                18: 'RAID 0+1',
                19: 'Concatenated RAID1',
                20: 'Concatenated RAID5',
                21: 'No RAID',
                22: 'RAID Morph',
                24: 'RAID60',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        disktable = tabledata.get('virtualDiskTable')
        rm = self.relMap()
        for oid, disk in disktable.iteritems():
            try:
                om = self.objectMap(disk)
                om.id = self.prepId(om.id)
                om.snmpindex = oid.strip('.')
                om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1), 'Unknown (%d)' % om.diskType)
                om.stripesize = getattr(om, '_stripesizeM', 0) * 1048576 + getattr(om, 'stripesize', 0)
                om.size = getattr(om, '_sizeM', 0) * 1048576 + getattr(om, 'size', 0)
            except AttributeError:
                continue
            rm.append(om)
        return rm
