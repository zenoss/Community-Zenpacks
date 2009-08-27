################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPExpansionCardMap

HPExpansionCardMap maps the cpqSePciSlotTable table to cards objects

$Id: HPExpansionCardMap.py,v 1.1 2009/08/18 16:40:53 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class HPExpansionCardMap(SnmpPlugin):
    """Map HP/Compaq insight manager PCI table to model."""

    maptype = "HPExpansionCardMap"
    modname = "ZenPacks.community.HPMon.cpqSePciSlot"
    relname = "cards"
    compname = "hw"
    deviceProperties = \
                SnmpPlugin.deviceProperties + ('zHPExpansionCardMapIgnorePci','zCollectorPlugins',)
    oms = {}

    snmpGetTableMaps = (
        GetTableMap('cpqSePciSlotTable',
	            '.1.3.6.1.4.1.232.1.2.13.1.1',
		    {
			'.3': 'slot',
			'.5': '_model',
		    }
	),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
	if not device.id in self.oms:
	    self.oms[device.id] = []
        rm = self.relMap()
	ignorepci = getattr(device, 'zHPExpansionCardMapIgnorePci', False)
	if not ignorepci:
            getdata, tabledata = results
            pcimap = {}
            pcicardtable = tabledata.get('cpqSePciSlotTable')
            for om in self.oms[device.id]:
    	        if om.modname == "ZenPacks.community.HPMon.cpqSiMemModule": continue
	        pcimap[int(om.slot)] = 1
            for oid, card in pcicardtable.iteritems():
                try:
                    om = self.objectMap(card)
		    om.snmpindex = oid.strip('.')
	            if int(om.slot) == 0: continue
                    if int(om.slot) in pcimap: continue
                    om.id = self.prepId("cpqSePciSlot%d" % om.slot)
                    om.setProductKey = "%s" % om._model
                except AttributeError:
                    continue
                self.oms[device.id].append(om)
	for om in self.oms[device.id]:
	    rm.append(om)
	del self.oms[device.id]
        return rm

