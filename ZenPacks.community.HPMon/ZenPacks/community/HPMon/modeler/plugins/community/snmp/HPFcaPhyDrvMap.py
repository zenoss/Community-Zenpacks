################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPFcaPhyDrvMap

HPFcaPhyDrvMap maps the cpqFcaPhyDrvTable to disks objects

$Id: HPFcaPhyDrvMap.py,v 1.1 2009/08/18 16:48:53 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPHardDiskMap import HPHardDiskMap

class HPFcaPhyDrvMap(HPHardDiskMap):
    """Map HP/Compaq insight manager DA Hard Disk tables to model."""

    maptype = "HPFcaPhyDrvMap"
    modname = "ZenPacks.community.HPMon.cpqFcaPhyDrv"

    snmpGetTableMaps = (
        GetTableMap('cpqFcaPhyDrvTable',
                    '.1.3.6.1.4.1.232.16.2.5.1.1',
                    {
                        '.1': 'chassis',
                        '.3': 'description',
                        '.4': 'FWRev',
                        '.5': 'bay',
                        '.6': 'status',
                        '.38': 'size',
                        '.40': 'hotPlug',
                        '.42': 'busNumber',
                        '.43': 'serialNumber',
                        '.50': 'rpm',
                        '.51': 'diskType',
                    }
        ),
        GetTableMap('cpqSsChassisTable',
                    '.1.3.6.1.4.1.232.8.2.2.1.1',
                    {
                        '.4': 'name',
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
        disktable = tabledata.get('cpqFcaPhyDrvTable')
        chassismap = {}
        chassistable = tabledata.get('cpqSsChassisTable')
        for oid, chassis in chassistable.iteritems():
            chassismap[oid.strip('.')] = chassis['name']
        external = 'community.snmp.HPSsChassisMap' in getattr(device, 'zCollectorPlugins', [])
        if not device.id in HPHardDiskMap.oms:
            HPHardDiskMap.oms[device.id] = []
        for oid, disk in disktable.iteritems():
            try:
                om = self.objectMap(disk)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("HardDisk%s" % om.snmpindex).replace('.', '_')
                if hasattr(om, 'vendor'):
                    om.description = "%s %s" % (om.vendor, om.description)
                om.setProductKey = om.description
                om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1), '%s (%d)' %(self.diskTypes[1], om.diskType))
                om.rpm = self.rpms.get(getattr(om, 'rpm', 1), om.rpm)
                om.size = "%d" % (getattr(om, 'size', 0) * 1048576)
                om.chassis = chassismap.get(om.chassis, '')
                om.external = external
            except AttributeError:
                continue
            HPHardDiskMap.oms[device.id].append(om)
        return
