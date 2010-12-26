################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CiscoFanMap

CiscoFanMap maps the ciscoEnvMonTemperatureStatusTable table to
temperaturesensors objects

$Id: CiscoFanMap.py,v 1.0 2010/12/06 14:34:47 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class CiscoFanMap(SnmpPlugin):
    """Map Cisco Environment Fans table to model."""

    maptype = "CiscoFanMap"
    modname = "ZenPacks.community.CiscoEnvMon.CiscoFan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('FanTable',
                    '.1.3.6.1.4.1.9.9.13.1.4.1',
                    {
                        '.2': 'id',
                        '.3': 'state',
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
        for oid, fan in tabledata.get("FanTable",{}).iteritems():
            try:
                om = self.objectMap(fan)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId(om.id)
                om.state = self.states.get(int(om.state), 'unknown')
            except AttributeError:
                continue
            rm.append(om)
        return rm
