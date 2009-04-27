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

$Id: HPMemoryModuleMap.py,v 1.0 2008/11/13 12:20:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

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
			'.4': 'moduletype',
			'.5': 'speed',
			'.7': '_manufacturer',
			'.10': 'serialNumber',
			'.13': 'frequency',
		    }
	),
        GetTableMap('cpqHeResMemModuleTable',
	            '.1.3.6.1.4.1.232.6.2.14.11.1',
		    {
		        '.1': '_boardindex',
			'.2': 'slot',
			'.4': 'status',
		    }
	),
    )

    moduletypes = {1: 'other',
		    2: 'Memory Board',
		    3: 'Compaq Single Width memory module',
		    4: 'Compaq Double Width memory module',
		    5: 'SIMM',
		    6: 'PCMCIA memory module',
		    7: 'Compaq Specific memory module',
		    8: 'DIMM',
		    9: 'Small Outline DIMM',
		    10: 'RIMM',
		    11: 'SRIMM',
		    12: 'FB-DIMM',
		    }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	mmstatustable = tabledata.get('cpqHeResMemModuleTable')
	cardtable = tabledata.get('cpqSiMemModuleTable')
	statusmap ={}
        rm = self.relMap()
#	if not device.id in HPExpansionCardMap.oms:
#	    HPExpansionCardMap.oms[device.id] = []
	for card in mmstatustable.values():
	    statusmap["%d.%d" % (int(card['_boardindex']), int(card['slot']))] = int(card['status'])
        for card in cardtable.values():
            try:
                om = self.objectMap(card)
		om.snmpindex = "%d.%d" % (om._boardindex, om.slot)
                om.id = self.prepId("cpqSiMemModule%s" % om.snmpindex)
		om.status = statusmap.get(om.snmpindex, 1)
		if hasattr(om, 'size'):
		    om.size = om.size * 1024
		om.moduletype = self.moduletypes.get(getattr(om, 'moduletype', 1), '%s (%d)' % (self.moduletypes[1], om.moduletype))
		if om.size > 0:
		    model = []
		    if not om.moduletype.startswith('Compaq'):
		        if len(getattr(om, '_manufacturer', 'Unknown')) > 0:
		            model.append(getattr(om, '_manufacturer', 'Unknown'))
		        else:
		            model.append('Unknown')
                    model.append(om.moduletype)
                    model.append(convToUnits(om.size))
		    if getattr(om, 'frequency', 0) > 0:
		        model.append("%sMHz" % getattr(om, 'frequency', 0))
                    om.setProductKey = "%s" % " ".join(model)
		else:
		    om.monitor = False
            except AttributeError:
                continue
            rm.append(om)
#            HPExpansionCardMap.oms[device.id].append(om)
	return rm

