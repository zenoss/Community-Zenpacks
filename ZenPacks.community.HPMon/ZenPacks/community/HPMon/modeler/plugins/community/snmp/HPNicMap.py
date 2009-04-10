################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPNicMap

HPNicMap maps the cpqNicIfPhysAdapterTable table to cpqNicIfPhysAdapter objects

$Id: HPNicMap.py,v 1.0 2008/11/13 12:20:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPExpansionCardMap import HPExpansionCardMap

class HPNicMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqNicIfPhysAdapterTable table to model."""

    maptype = "cpqNicIfPhysAdapter"
    modname = "ZenPacks.community.HPMon.cpqNicIfPhysAdapter"

    snmpGetTableMaps = (
        GetTableMap('cpqNicIfPhysAdapterTable',
	            '.1.3.6.1.4.1.232.18.2.3.1.1',
		    {
		        '.1': 'snmpindex',
			'.3': 'role',
			'.4': 'macaddress',
			'.5': 'slot',
			'.7': '_irq',
			'.10': 'port',
			'.11': 'duplex',
			'.14': 'status',
			'.33': 'speed',
			'.39': 'model',
		    }
	),
        GetTableMap('cpqSePciSlotTable',
	            '.1.3.6.1.4.1.232.1.2.13.1.1',
		    {
		        '.1': 'busnumber',
			'.2': 'snmpindex',
			'.3': 'slot',
			'.5': '_model',
		    }
	),
        GetTableMap('cpqSePciFunctTable',
	            '.1.3.6.1.4.1.232.1.2.13.2.1',
		    {
		        '.1': 'busnumber',
			'.2': 'snmpindex',
			'.4': 'classcode',
			'.9': 'int',
		    }
	),
    )

    roles = {1: 'unknown',
	    2: 'Primary',
	    3: 'Secondary',
	    4: 'Member',
	    5: 'TxRx',
	    6: 'Tx',
	    7: 'Standby',
	    8: 'None',
	    255: 'Not Applicable',
	    }

    duplexs =  {1: 'other',
		2: 'Half',
		3: 'Full',
		}

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	if not device.id in HPExpansionCardMap.oms:
	    HPExpansionCardMap.oms[device.id] = []
	cardtable = tabledata.get('cpqNicIfPhysAdapterTable')
        pcicardtable = tabledata.get('cpqSePciSlotTable')
        pciirqcardtable = tabledata.get('cpqSePciFunctTable')
	pciirqmap = {}
        if pcicardtable and pciirqcardtable:
	    pcinamesmap = {}
            for pci in pcicardtable.values():
	        pcinamesmap["%d.%d" % (pci['busnumber'], pci['snmpindex'])] = pci['_model']
            for pciirq in pciirqcardtable.values():
	        try:
	            pciirqmap[self.asmac(pciirq['classcode'])][pciirq['int']] = pcinamesmap["%d.%d" % (pciirq['busnumber'], pciirq['snmpindex'])]
		except:
	            pciirqmap[self.asmac(pciirq['classcode'])] = {}
	            pciirqmap[self.asmac(pciirq['classcode'])][pciirq['int']] = pcinamesmap["%d.%d" % (pciirq['busnumber'], pciirq['snmpindex'])]
        for card in cardtable.values():
            try:
                om = self.objectMap(card)
		om.snmpindex = "%s" % om.snmpindex
                om.slot = getattr(om, 'slot', 0)
		if int(om.slot) < 0: continue
                om.port = getattr(om, 'port', 0)
                om.id = self.prepId("cpqNicIfPhysAdapter%d_%d" % (om.slot, om.port))
		if not hasattr(om, 'model'):
		    try:
		        om.model = pciirqmap['00:00:02'][om._irq]
		    except:
		        om.model = "Unknown Network Adapter"
		om.duplex = self.duplexs.get(getattr(om, 'duplex', 1), 'other')
                om.setProductKey = "%s" % om.model
		om.role = self.roles.get(getattr(om, 'role', 1), '%s (%d)'%(self.roles[1], om.role))
		if hasattr(om, 'macaddress'):
                    om.macaddress = self.asmac(om.macaddress)
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
	return

