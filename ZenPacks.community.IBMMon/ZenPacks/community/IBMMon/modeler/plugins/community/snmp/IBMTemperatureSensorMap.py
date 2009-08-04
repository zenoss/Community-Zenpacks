################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMTemperatureSensorMap

IBMTemperatureSensorMap maps the iBMPSGTemperatureSensorTable table to
temperaturesensors objects

$Id: IBMTemperatureSensorMap.py,v 1.0 2009/07/12 23:36:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class IBMTemperatureSensorMap(SnmpPlugin):
    """Map IBM Director Temperature Sensors table to model."""

    maptype = "IBMTemperatureSensorMap"
    modname = "ZenPacks.community.IBMMon.IBMTemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('temperatureProbeTable',
	            '1.3.6.1.4.1.2.6.159.1.1.80.1.1',
		    {
		        '.1': 'id',
			'.14': 'threshold',
			'.17': '_location',
		    }
	),
    )

    locations = {0: "Unknown",
                 1: "Motherboard",
                 2: "CPU",
                 3: "PowerSupply",
                 4: "DASD",
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        tsensorstable = tabledata.get("temperatureProbeTable")
        rm = self.relMap()
	localecounter = {}
        for oid, tsensor in tsensorstable.iteritems():
            try:
                om = self.objectMap(tsensor)
		om.snmpindex =  oid.strip('.')
		if om._location in localecounter:
		    localecounter[om._location] = localecounter[om._location] + 1
		else:
		    localecounter[om._location] = 1
                om.id = self.prepId("%s%d" % (self.locations.get(getattr(om, '_location', 1), self.locations[1]), localecounter[om._location]))
                om.status = 2
            except AttributeError:
                continue
            rm.append(om)
        return rm
