################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPSasLogDrvMap

HPSasLogDrvMap maps the cpqSasLogDrvTable to disks objects

$Id: HPSasLogDrvMap.py,v 1.0 2008/11/13 12:20:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPHardDiskMap import HPHardDiskMap

class HPSasLogDrvMap(HPHardDiskMap):
    """Map HP/Compaq insight manager DA Logical Disk tables to model."""

    maptype = "HPSasLogDrvMap"
    modname = "ZenPacks.community.HPMon.cpqSasLogDrv"

    snmpGetTableMaps = (
        GetTableMap('cpqSasLogDrvTable',
	            '.1.3.6.1.4.1.232.5.5.3.1.1',
		    {
		        '.1': '_cntrlindex',
			'.2': 'snmpindex',
			'.3': 'diskType',
			'.4': 'status',
			'.7': 'size',
			'.6': 'stripesize',
			'.11': 'description',
		    }
	),
    )

    diskTypes = {1: 'other',
		2: 'RAID0',
		3: 'RAID1',
		}

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	disktable = tabledata.get('cpqSasLogDrvTable')
	if not device.id in HPHardDiskMap.oms:
	    HPHardDiskMap.oms[device.id] = []
        for disk in disktable.values():
            try:
                om = self.objectMap(disk)
		om.snmpindex =  "%d.%d" % (om._cntrlindex, om.snmpindex)
                om.id = self.prepId("LogicalDisk%s" % om.snmpindex).replace('.', '_')
		om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1), '%s (%d)' %(self.diskTypes[1], om.diskType))
		om.stripesize = "%d" % (getattr(om, 'stripesize', 0) * 1024)
		om.size = "%d" % (getattr(om, 'size', 0) * 1048576)
            except AttributeError:
                continue
            HPHardDiskMap.oms[device.id].append(om)
	return
