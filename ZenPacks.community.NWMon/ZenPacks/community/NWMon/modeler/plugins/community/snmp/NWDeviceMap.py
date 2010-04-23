################################################################################
#
# This program is part of the NWMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""NWDeviceMap

NWDeviceMap maps the interface and ip tables to interface objects

$Id: NWDeviceMap.py,v 1.0 2008/11/18 14:37:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class NWDeviceMap(SnmpPlugin):

    maptype = 'DeviceMap'

    columns = {
             '.1.3.6.1.4.1.23.2.79.6.1.0' : 'totalMemory',
             '.1.3.6.1.4.1.23.2.79.7.1.5.0' : 'totalSwap',
             }
    snmpGetMap = GetMap(columns)


    def process(self, device, results, log):
        """collect snmp information from this device"""
        import re
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        om = self.objectMap(getdata)
        om.totalSwap = om.totalSwap * 4096
        maps = []
        if om.totalMemory > 0:
            maps.append(ObjectMap({"totalMemory": long(om.totalMemory)}, compname="hw"))
        maps.append(ObjectMap({"totalSwap": om.totalSwap}, compname="os"))
        return maps


