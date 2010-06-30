################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPMemoryModuleMap

HPMemoryModuleMap maps the cpqSiMemModuleTable table to cpqSiMemModule objects

$Id: HPMemoryModuleMap.py,v 1.1 2009/08/18 16:53:53 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class HPMemoryModuleMap(SnmpPlugin):
    """Map HP/Compaq insight manager cpqSiMemModuleTable table to model."""

    maptype = "cpqSiMemModule"
    modname = "ZenPacks.community.HPMon.cpqSiMemModule"
    relname = "memorymodules"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('cpqSiMemModuleTable',
                    '.1.3.6.1.4.1.232.2.2.4.5.1',
                    {
                        '.1': '_boardindex',
                        '.2': 'slot',
                        '.3': 'size',
                        '.4': '_slottype',
                        '.5': '_speed',
                        '.6': '_technology',
                        '.7': '_manufacturer',
                        '.10': 'serialNumber',
                        '.13': '_frequency',
                    }
        ),
        GetTableMap('cpqHeResMemModuleTable',
                    '.1.3.6.1.4.1.232.6.2.14.11.1',
                    {
                        '.4': 'status',
                    }
        ),
    )

    slottypes = {1: 'Slot',
                2: 'OnBoard',
                3: 'SingleWidth',
                4: 'DoubleWidth',
                5: 'SIMM',
                6: 'PCMCIA',
                7: 'COMPAQ',
                8: 'DIMM',
                9: 'SO-DIMM',
                10: 'RIMM',
                11: 'SRIMM',
                12: 'FB-DIMM',
                }

    technologies = { 1: 'other',
                    2: 'FPM',
                    3: 'EDO',
                    4: 'burstEDO',
                    5: 'DDR',
                    6: 'RDRAM',
                    }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        mmstatustable = tabledata.get('cpqHeResMemModuleTable')
        cardtable = tabledata.get('cpqSiMemModuleTable')
        statusmap ={}
        rm = self.relMap()
        for oid, card in mmstatustable.iteritems():
            statusmap[oid.strip('.')] = int(card['status'])
        for oid, card in cardtable.iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = '%s.%s'%(om._boardindex, om.slot)
                om.id = self.prepId("Board%d %s%d" % (om._boardindex,
                                        self.slottypes.get(om._slottype,'Slot'),
                                        om.slot))
                om.status = statusmap.get(om.snmpindex, None)
                if not om.status:
                    om.status = 1
                    om.monitor = False
                if hasattr(om, 'size'):
                    om.size = om.size * 1024
                if om.size > 0:
                    model = []
                    if getattr(om, '_manufacturer', '') != '':
                        model.append(getattr(om, '_manufacturer', ''))
                    if self.technologies.get(om._technology, '') != '':
                        model.append(self.technologies.get(om._technology, ''))
                    if self.slottypes.get(om._slottype, '') != '' and om._slottype > 1:
                        model.append(self.slottypes.get(om._slottype, ''))
                    model.append(convToUnits(om.size))
                    if getattr(om, '_frequency', 0) > 0:
                        model.append("%sMHz" % getattr(om, '_frequency', 0))
                    if getattr(om, '_speed', 0) > 0:
                        model.append("%sns" % getattr(om, '_speed', 0))
                    om.setProductKey = "%s" % " ".join(model)
                else:
                    om.monitor = False
            except AttributeError:
                continue
            rm.append(om)
        return rm

