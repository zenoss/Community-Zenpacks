################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMDeviceMap

IBMDeviceMap maps mib elements from IBM Director mib to get hw and os products.

$Id: IBMDeviceMap.py,v 1.0 2009/07/12 23:08:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class IBMDeviceMap(SnmpPlugin):
    """Map mib elements from IBM Director mib to get hw and os products.
    """

    maptype = "IBMDeviceMap" 

    snmpGetMap = GetMap({ 
        '.1.3.6.1.4.1.2.6.159.1.1.60.1.1.5.6.115.121.115.116.101.109' : 'setHWProductKey',
        '.1.3.6.1.4.1.2.6.159.1.1.60.1.1.3.6.115.121.115.116.101.109' : 'setHWSerialNumber',
         })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
        om = self.objectMap(getdata)
        om.setHWProductKey = MultiArgs(om.setHWProductKey, "IBM")
        return om

