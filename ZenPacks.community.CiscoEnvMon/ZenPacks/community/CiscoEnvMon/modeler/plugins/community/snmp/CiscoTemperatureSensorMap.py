################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CiscoTemperatureSensorMap

CiscoTemperatureSensorMap maps the ciscoEnvMonTemperatureStatusTable table to
temperaturesensors objects

$Id: CiscoTemperatureSensorMap.py,v 1.0 2010/12/06 14:34:47 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class CiscoTemperatureSensorMap(SnmpPlugin):
    """Map Cisco Environment Temperature Sensors table to model."""

    maptype = "CiscoTemperatureSensorMap"
    modname = "ZenPacks.community.CiscoEnvMon.CiscoTemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('TemperatureTable',
                    '.1.3.6.1.4.1.9.9.13.1.3.1',
                    {
                        '.2': 'id',
                        '.6': 'state',
                    }
        ),
    )

    states  =  {1:'normal',
                2:'warning',
                3:'critical',
                4:'shutdown',
                5:'notPresent',
                6:'notFunctioning',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, tsensor in tabledata.get("TemperatureTable",{}).iteritems():
            try:
                om = self.objectMap(tsensor)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId(om.id)
                om.state = self.states.get(int(om.state), 'unknown')
            except AttributeError:
                continue
            rm.append(om)
        return rm
