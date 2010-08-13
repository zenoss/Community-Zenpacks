################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellHardDiskMap

DellHardDiskMap maps the arrayDisktable to disks objects

$Id: DellHardDiskMap.py,v 1.2 2010/08/14 00:08:40 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class DellHardDiskMap(SnmpPlugin):
    """Map Dell System Management Hard Disk table to model."""

    maptype = "DellHardDiskMap"
    modname = "ZenPacks.community.DellMon.DellHardDisk"
    relname = "harddisks"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('arrayDiskTable',
                    '1.3.6.1.4.1.674.10893.1.20.130.4.1',
                    {
                        '.1': 'snmpindex',
                        '.2': 'description',
                        '.3': '_manuf',
                        '.4': 'status',
                        '.6': '_model',
                        '.7': 'serialNumber',
                        '.8': 'FWRev',
                        '.11': '_sizeM',
                        '.12': 'size',
                        '.15': 'bay',
                        '.21': 'diskType',
                        '.30': 'rpm',
                    }
        ),
        GetTableMap('arrayLocationTable',
                    '1.3.6.1.4.1.674.10893.1.20.130.5.1',
                    {
                        '.1': 'snmpindex',
                        '.4': 'chassis',
                    }
        ),
    )

    diskTypes = {1: 'SCSI',
                2: 'IDE',
                3: 'FC',
                4: 'SSA',
                5: '',
                6: 'USB',
                7: 'SATA',
                8: 'SAS',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        disktable = tabledata.get('arrayDiskTable')
        if not disktable: return
        diskLocation = tabledata.get('arrayLocationTable')
        rm = self.relMap()
        for disk, location in zip(disktable.values(), diskLocation.values()):
            try:
                om = self.objectMap(disk)
                chassis = location.get('chassis', 'Backplane')
                om.id = self.prepId("%s %s" % (chassis, om.description))
                om._model = getattr(om, '_model', 'hard disk')
                om._manuf = getattr(om, '_manuf', 'Unknown')
                om.description = "%s %s" % (om._manuf, om._model)
                om.setProductKey = MultiArgs(om._model, om._manuf)
                om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1), '%s (%d)' %(self.diskTypes[1], om.diskType))
                om.size = "%d" % (getattr(om, '_sizeM', 0) * 1048576 + getattr(om, 'size', 0))
            except AttributeError:
                continue
            rm.append(om)
        return rm
