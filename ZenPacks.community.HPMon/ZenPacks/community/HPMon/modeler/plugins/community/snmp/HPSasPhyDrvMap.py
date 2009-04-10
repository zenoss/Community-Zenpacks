################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPSasPhyDrvMap

HPSasPhyDrvMap maps the cpqSasPhyDrvTable to disks objects

$Id: HPSasPhyDrvMap.py,v 1.0 2008/11/13 12:20:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPHardDiskMap import HPHardDiskMap

class HPSasPhyDrvMap(HPHardDiskMap):
    """Map HP/Compaq insight manager DA Hard Disk tables to model."""

    maptype = "HPSasPhyDrvMap"
    modname = "ZenPacks.community.HPMon.cpqSasPhyDrv"

    snmpGetTableMaps = (
        GetTableMap('cpqSasPhyDrvTable',
	            '.1.3.6.1.4.1.232.5.5.2.1.1',
		    {
		        '.1': '_cntrlindex',
			'.2': 'snmpindex',
			'.3': 'bay',
			'.4': 'description',
			'.5': 'status',
			'.7': 'FWRev',
			'.8': 'size',
			'.10': 'serialNumber',
			'.12': 'rpm',
			'.15': 'hotPlug',
			'.16': 'diskType',
		    }
	),
    )

    diskTypes = {1: 'other',
		2: 'SAS',
		3: 'SATA',
		}

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	disktable = tabledata.get('cpqSasPhyDrvTable')
	if not device.id in HPHardDiskMap.oms:
	    HPHardDiskMap.oms[device.id] = []
        for disk in disktable.values():
            try:
                om = self.objectMap(disk)
		om.snmpindex =  "%d.%d" % (om._cntrlindex, om.snmpindex)
                om.id = self.prepId("HardDisk%s" % om.snmpindex).replace('.', '_')
		if hasattr(om, 'vendor'):
		    om.description = "%s %s" % (om.vendor, om.description)
                om.setProductKey = om.description
		om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1), '%s (%d)' %(self.diskTypes[1], om.diskType))
		om.rpm = self.rpms.get(getattr(om, 'rpm', 1), om.rpm)
		om.size = "%d" % (getattr(om, 'size', 0) * 1048576)
            except AttributeError:
                continue
            HPHardDiskMap.oms[device.id].append(om)
	return
