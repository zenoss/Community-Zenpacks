################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellTemperatureSensorMap

DellTemperatureSensorMap maps the cpqHeTemperatureTable table to temperaturesensors objects

$Id: DellTemperatureSensorMap.py,v 1.0 2009/06/22 22:53:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class DellTemperatureSensorMap(SnmpPlugin):
    """Map Dell System Management Temperature Sensors table to model."""

    maptype = "DellTemperatureSensorMap"
    modname = "ZenPacks.community.DellMon.DellTemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('temperatureProbeTable',
	            '.1.3.6.1.4.1.674.10892.1.700.20.1',
		    {
		        '.1': '_chassis',
			'.2': 'snmpindex',
			'.5': 'status',
			'.7': '_type',
			'.8': '_location',
			'.10': 'threshold',
		    }
	),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        tsensorstable = tabledata.get("temperatureProbeTable")
        rm = self.relMap()
        for tsensor in tsensorstable.values():
            try:
                om = self.objectMap(tsensor)
		if om.status < 3: continue
		om.snmpindex =  "%d.%d" % (om._chassis, om.snmpindex)
		if om._type == 16:
                    om.modname = "ZenPacks.community.DellMon.DellDiscreteTemperatureSensor"
                    om.threshold = 1
                om.id = self.prepId(getattr(om, '_location', 'Unknown'))
            except AttributeError:
                continue
            rm.append(om)
        return rm
