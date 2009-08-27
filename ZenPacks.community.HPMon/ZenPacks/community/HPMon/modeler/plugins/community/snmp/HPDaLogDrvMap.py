################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPDaLogDrvMap

HPDaLogDrvMap maps the cpqDaLogDrvTable to disks objects

$Id: HPDaLogDrvMap.py,v 1.1 2009/08/18 16:39:53 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPLogicalDiskMap import HPLogicalDiskMap

class HPDaLogDrvMap(HPLogicalDiskMap):
    """Map HP/Compaq insight manager DA Logical Disk tables to model."""

    maptype = "HPDaLogDrvMap"
    modname = "ZenPacks.community.HPMon.cpqDaLogDrv"

    snmpGetTableMaps = (
        GetTableMap('cpqDaLogDrvTable',
	            '.1.3.6.1.4.1.232.3.2.3.1.1',
		    {
			'.3': 'diskType',
			'.4': 'status',
			'.9': 'size',
			'.13': 'stripesize',
			'.14': 'description',
		    }
	),
    )

    diskTypes = {1: 'other',
		2: 'RAID0',
		3: 'RAID1',
		4: 'RAID10',
		5: 'RAID5',
		6: 'RAID1E',
		7: 'RAID ADG',
		}

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	disktable = tabledata.get('cpqDaLogDrvTable')
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
