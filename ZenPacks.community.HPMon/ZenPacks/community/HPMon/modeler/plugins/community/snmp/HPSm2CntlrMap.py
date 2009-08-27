################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPSm2CntlrMap

HPSm2CntlrMap maps the cpqSm2CntlrTable table to cpqSm2Cntlr objects

$Id: HPSm2CntlrMap.py,v 1.0 2008/11/13 12:20:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPExpansionCardMap import HPExpansionCardMap

class HPSm2CntlrMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqSm2CntlrTable table to model."""

    maptype = "cpqSm2Cntlr"
    modname = "ZenPacks.community.HPMon.cpqSm2Cntlr"

    snmpGetTableMaps = (
        GetTableMap('cpqSm2CntlrTable',
	            '.1.3.6.1.4.1.232.9.2.2',
		    {
		        '.2': 'romRev',
			'.12': 'status',
			'.15': 'serialNumber',
			'.18': 'systemId',
			'.21': 'model',
			'.28': 'hwVer',
		    }
	),
        GetTableMap('cpqSm2NicConfigTable',
	            '.1.3.6.1.4.1.232.9.2.5.1.1',
		    {
		        '.1': 'snmpindex',
			'.2': 'model',
			'.4': 'macaddress',
			'.5': 'ipaddress',
			'.6': 'subnetmask',
			'.14': 'dnsName',
		    }
	),
    )

    models =   {1: 'Unknown Integrated Lights-Out Board',
                2: 'Compaq EISA Remote Insight Board',
                3: 'Compaq PCI Remote Insight Board',
                4: 'Compaq PCI Remote Insight Lights-Out Edition Board',
                5: 'Compaq Integrated Remote Insight Lights-Out Edition Board',
                6: 'Compaq Integrated Remote Insight Lights-Out Edition Ver.II Board',
                7: 'HP Integrated Lights-Out 2 Edition Board',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	cardtable = tabledata.get('cpqSm2CntlrTable')
	iloniccardtable = tabledata.get('cpqSm2NicConfigTable')
	if not device.id in HPExpansionCardMap.oms:
	    HPExpansionCardMap.oms[device.id] = []
        for oid, card in cardtable.iteritems():
            try:
                om = self.objectMap(card)
		om.snmpindex = oid.strip('.')
                om.id = self.prepId("cpqSm2Cntlr%s" % om.snmpindex)
                om.slot = getattr(om, 'slot', 0)
		om.model = self.models.get(getattr(om, 'model', 1), '%s (%d)' %(self.models[1], om.model))
                om.setProductKey = "%s" % om.model
		for nic in iloniccardtable.values():
#		    om.nicmodel = nic['model']
		    om.macaddress = self.asmac(nic['macaddress'])
		    om.ipaddress = nic['ipaddress']
		    om.subnetmask = nic['subnetmask']
		    om.dnsName = nic['dnsName']
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
	return

