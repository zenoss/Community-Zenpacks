################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellDeviceMap

DellDeviceMap.

$Id: DellDeviceMap.py,v 1.1 2010/08/13 23:59:12 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs


class DellDeviceMap(SnmpPlugin):
    """Map mib elements from Dell Open Manage mib to get hw and os products.
    """

    maptype = "DellDeviceMap" 

    snmpGetMap = GetMap({ 
        '.1.3.6.1.4.1.674.10892.1.400.10.1.6.1': 'setOSProductKey',
        '.1.3.6.1.4.1.674.10892.1.300.10.1.9.1' : 'setHWProductKey',
        '.1.3.6.1.4.1.674.10892.1.300.10.1.11.1' : 'setHWSerialNumber',
         })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
        om = self.objectMap(getdata)
        om.setHWProductKey = MultiArgs(om.setHWProductKey, "Dell")
        return om

