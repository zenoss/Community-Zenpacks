################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellMemoryModuleMap

DellMemoryModuleMap maps the memoryDeviceTable table to DellMemoryModule objects

$Id: DellMemoryModuleMap.py,v 1.2 2010/08/14 00:15:57 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class DellMemoryModuleMap(SnmpPlugin):
    """Map Dell System Management Memory Module table to model."""

    maptype = "DellMemoryModule"
    modname = "ZenPacks.community.DellMon.DellMemoryModule"
    relname = "memorymodules"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('memoryDeviceTable',
                    '.1.3.6.1.4.1.674.10892.1.1100.50.1',
                    {
                        '.5': 'status',
                        '.7': 'moduletype',
                        '.8': '_location',
                        '.14': 'size',
                        '.21': '_manuf',
                        '.22': '_pnumber',
                        '.23': 'serialNumber',
                        '.25': 'speed',
                    }
        ),
    )

    moduletypes = {1: 'Other',
                    2: 'Unknown',
                    3: 'DRAM',
                    4: 'EDRAM',
                    5: 'VRAM',
                    6: 'SRAM',
                    7: 'RAM',
                    8: 'ROM',
                    9: 'FLASH',
                    10: 'EEPROM',
                    11: 'FEPROM',
                    12: 'EPROM',
                    13: 'CDROM',
                    14: '3DRAM',
                    15: 'SDRAM',
                    16: 'SGRAM',
                    17: 'RDRAM',
                    18: 'DDR',
                    19: 'DDR2',
                    20: 'DDR3',
                    }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cardtable = tabledata.get('memoryDeviceTable')
        rm = self.relMap()
        for oid, card in cardtable.iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId(getattr(om, '_location', 'Unknown').strip())
                if hasattr(om, 'size'):
                    om.size = om.size * 1024
                om.moduletype = self.moduletypes.get(getattr(om, 'moduletype', 1),
                                '%s (%d)' % (self.moduletypes[1], om.moduletype))
                if om.size > 0:
                    model = []
                    om._manuf=getattr(om,'_manuf','Unknown').split('(')[0].strip()
                    if not om._manuf: om._manuf = 'Unknown'
                    model.append(om._manuf)
                    model.append(om.moduletype)
                    model.append(convToUnits(om.size))
                    if getattr(om, 'frequency', 0) > 0:
                        model.append("%sMHz" % getattr(om, 'frequency', 0))
                    om.setProductKey = MultiArgs("%s" % " ".join(model), om._manuf)
                else:
                    om.monitor = False
            except AttributeError:
                continue
            rm.append(om)
        return rm

