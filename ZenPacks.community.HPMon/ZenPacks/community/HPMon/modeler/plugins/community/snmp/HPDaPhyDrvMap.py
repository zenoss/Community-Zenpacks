################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPDaPhyDrvMap

HPDaPhyDrvMap maps the cpqDaPhyDrvTable to disks objects

$Id: HPDaPhyDrvMap.py,v 1.0 2008/11/13 12:20:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPHardDiskMap import HPHardDiskMap

class HPDaPhyDrvMap(HPHardDiskMap):
    """Map HP/Compaq insight manager DA Hard Disk tables to model."""

    maptype = "HPDaPhyDrvMap"
    modname = "ZenPacks.community.HPMon.cpqDaPhyDrv"

    snmpGetTableMaps = (
        GetTableMap('cpqDaPhyDrvTable',
	            '.1.3.6.1.4.1.232.3.2.5.1.1',
		    {
		        '.1': '_cntrlindex',
			'.2': 'snmpindex',
			'.3': 'description',
			'.4': 'FWRev',
			'.5': 'bay',
			'.6': 'status',
			'.45': 'size',
			'.48': 'hotPlug',
			'.51': 'serialNumber',
			'.59': 'rpm',
			'.60': 'diskType',
		    }
	),
    )

    diskTypes = {1: 'other',
		2: 'SCSI',
		3: 'SATA',
		4: 'SAS',
		}

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	disktable = tabledata.get('cpqDaPhyDrvTable')
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
