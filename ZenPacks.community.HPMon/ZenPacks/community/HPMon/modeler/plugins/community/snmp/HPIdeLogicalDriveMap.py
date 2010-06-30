################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPIdeLogicalDriveMap

HPIdeLogicalDriveMap maps the cpqIdeLogicalDriveTable to disks objects

$Id: HPIdeLogicalDriveMap.py,v 1.1 2009/08/18 16:51:53 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPLogicalDiskMap import HPLogicalDiskMap

class HPIdeLogicalDriveMap(HPLogicalDiskMap):
    """Map HP/Compaq insight manager DA Logical Disk tables to model."""

    maptype = "HPIdeLogicalDriveMap"
    modname = "ZenPacks.community.HPMon.cpqIdeLogicalDrive"

    snmpGetTableMaps = (
        GetTableMap('cpqIdeLogicalDriveTable',
                    '.1.3.6.1.4.1.232.14.2.6.1.1',
                    {
                        '.3': 'diskType',
                        '.4': 'size',
                        '.5': 'status',
                        '.8': 'stripesize',
                        '.11': 'description',
                    }
        ),
    )

    diskTypes = {1: 'other',
                2: 'RAID0',
                3: 'RAID1',
                4: 'RAID1+0',
                5: 'RAID5',
                6: 'RAID1+5',
                7: 'VOLUME',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        disktable = tabledata.get('cpqIdeLogicalDriveTable')
        if not device.id in HPLogicalDiskMap.oms:
            HPLogicalDiskMap.oms[device.id] = []
        for oid, disk in disktable.iteritems():
            try:
                om = self.objectMap(disk)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("LogicalDisk%s" % om.snmpindex).replace('.', '_')
                om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1), '%s (%d)' %(self.diskTypes[1], om.diskType))
                om.stripesize = "%d" % (getattr(om, 'stripesize', 0) * 1024)
                om.size = "%d" % (getattr(om, 'size', 0) * 1048576)
            except AttributeError:
                continue
            HPLogicalDiskMap.oms[device.id].append(om)
        return
