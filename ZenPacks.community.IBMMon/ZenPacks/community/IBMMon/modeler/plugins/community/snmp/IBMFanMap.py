################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMFanMap

IBMFanMap maps the iBMPSGTachometerTable table to fab objects

$Id: IBMFanMap.py,v 1.0 2009/07/13 00:27:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class IBMFanMap(SnmpPlugin):
    """Map IBM Director Fans table to model."""

    maptype = "IBMFanMap"
    modname = "ZenPacks.community.IBMMon.IBMFan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('fanTable',
	            '1.3.6.1.4.1.2.6.159.1.1.80.5.1',
		    {
		        '.1': 'id',
			'.5': 'type',
			'.12': 'threshold',
		    }
	),
    )


    types ={0: 'Unknown', 
            1: 'System Fan',
            2: 'PowerSupply Fan',
            3: 'CPU Fan',
            }


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        fantable = tabledata.get('fanTable')
        for oid, fan in fantable.iteritems():
            try:
                om = self.objectMap(fan)
		om.snmpindex =  oid.strip('.')
	        om.type = self.types.get(getattr(om, 'type', 2), 'Unknown')
                om.id = self.prepId(om.id)
                om.status = 2
            except AttributeError:
                continue
            rm.append(om)
        return rm
