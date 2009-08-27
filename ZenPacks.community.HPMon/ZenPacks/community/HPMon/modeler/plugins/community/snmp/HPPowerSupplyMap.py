################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPPowerSupplyMap

HPPowerSupplyMap maps the cpqHeFltTolPowerSupplyTable table to powersupplies objects

$Id: HPPowerSupplyMap.py,v 1.1 2009/08/18 16:58:53 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class HPPowerSupplyMap(SnmpPlugin):
    """Map HP/Compaq insight manager Power Supplies table to model."""

    maptype = "HPPowerSupplyMap"
    modname = "ZenPacks.community.HPMon.HPPowerSupply"
    relname = "powersupplies"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('cpqHeFltTolPowerSupplyTable',
	            '.1.3.6.1.4.1.232.6.2.9.3.1',
		    {
			'.3': '_present',
			'.5': 'status',
			'.6': 'millivolts',
			'.8': 'watts',
			'.11': 'serialNumber',
			'.13': 'type',
		    }
	),
    )

    typemap =  {1: 'other',
                2: 'Non Hot-pluggable Power Supply',
                3: 'Hot-pluggable Power Supply',
		}

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        pstable = tabledata.get('cpqHeFltTolPowerSupplyTable')
        for oid, ps in pstable.iteritems():
            try:
                om = self.objectMap(ps)
		if om._present < 3: continue
		om.snmpindex = oid.strip('.')
                om.id = self.prepId("PSU%s" % om.snmpindex.replace('.', '_'))
                om.type = "%s" % self.typemap.get(getattr(om, 'type', 1), '%s (%d)' %(self.typemap[1], om.type))
            except AttributeError:
                continue
            rm.append(om)
        return rm
