################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMNetworkAdapterMap

IBMNetworkAdapterMap maps the ibmSystemLogicalNetworkAdapterTable table to cards
objects

$Id: IBMNetworkAdapterMap.py,v 1.0 2009/07/21 23:36:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class IBMNetworkAdapterMap(SnmpPlugin):
    """Map IBM Director PCI table to model."""

    maptype = "IBMNetworkAdapterMap"
    modname = "ZenPacks.community.IBMMon.IBMNetworkAdapter"
    relname = "cards"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('networkAdapterTable',
	            '.1.3.6.1.4.1.2.6.159.1.1.110.1.1',
		    {
			'.1': 'id',
			'.3': 'model',
			'.7': 'macaddress',
			'.8': 'speed',
		    }
	),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        getdata, tabledata = results
        cardtable = tabledata.get('networkAdapterTable')
        for oid, card in cardtable.iteritems():
            try:
                om = self.objectMap(card)
		om.snmpindex =  oid.strip('.')
                om.id = self.prepId(om.id)
                om.slot = 0
                om.setProductKey = MultiArgs(om.model, om.model.split()[0]) 
		if hasattr(om, 'macaddress'):
		    mac = []
		    for i in range(6):
		        mac.append(om.macaddress[i*2:i*2+2])
                    om.macaddress = ':'.join(mac)
		if hasattr(om, 'speed'):
                    om.speed = int(om.speed) * 1000000
                om.status = 2
            except AttributeError:
                continue
            rm.append(om)
        return rm
