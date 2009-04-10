################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPSasHbaMap

HPSasHbaMap maps the cpqSasHbaTable table to cpqSasHba objects

$Id: HPSasHbaMap.py,v 1.0 2008/11/13 12:20:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPExpansionCardMap import HPExpansionCardMap

class HPSasHbaMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqSasHbaTable table to model."""

    maptype = "cpqSasHba"
    modname = "ZenPacks.community.HPMon.cpqSasHba"

    snmpGetTableMaps = (
        GetTableMap('cpqSasHbaTable',
	            '.1.3.6.1.4.1.232.5.5.1.1.1',
		    {
		        '.1': 'snmpindex',
			'.2': 'slot',
			'.3': 'model',
			'.4': 'status',
			'.7': 'serialNumber',
			'.8': 'FWRev',
		    }
	),
    )

    models =   {1: 'other',
                2: 'Unknown SAS HBA',
                3: 'HP 8 Internal Port SAS HBA with RAID',
                4: 'HP 4 Internal Port SAS HBA with RAID',
                5: 'HP SC44Ge Host Bus Adapter',
                6: 'HP SC40Ge HBA',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	cardtable = tabledata.get('cpqSasHbaTable')
	if not device.id in HPExpansionCardMap.oms:
	    HPExpansionCardMap.oms[device.id] = []
        for card in cardtable.values():
            try:
                om = self.objectMap(card)
		om.snmpindex = "%s" %om.snmpindex
                om.id = self.prepId("cpqSasHba%s" % om.snmpindex)
                om.slot = getattr(om, 'slot', 0)
		om.model = self.models.get(getattr(om, 'model', 2), '%s (%d)' %(self.models[2], om.model))
                om.setProductKey = "%s" % om.model
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
	return

