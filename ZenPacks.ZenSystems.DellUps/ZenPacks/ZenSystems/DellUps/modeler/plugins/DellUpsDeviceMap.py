##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 8th, 2011
# Revised:
#
# DellUpsDevice modler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """DellUpsDeviceMap

Gather information from Dell UPS devices.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
import re

class DellUpsDeviceMap(SnmpPlugin):
    maptype = "DellUpsDeviceMap"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.674.10902.2.120.1.1.0': 'setHWProductKey',
        '.1.3.6.1.4.1.674.10902.2.100.5.0': 'setOSProductKey',
        '.1.3.6.1.4.1.674.10902.2.120.1.2.0': 'setHWSerialNumber',
         })

    def condition(self, device, log):
        """only for boxes with proper object id
        """
        return device.snmpOid.startswith(".1.3.6.1.4.1.674.10902.2")


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        om = self.objectMap(getdata)
        manufacturer = "Dell"
        om.setHWProductKey = MultiArgs(om.setHWProductKey, manufacturer)
#        log.debug("HWProductKey=%s Manufacturer = %s" % (om.setHWProductKey, manufacturer))
        om.setOSProductKey = MultiArgs(om.setOSProductKey, manufacturer)
#        log.debug("OSProductKey=%s Manufacturer = %s" % (om.setOSProductKey, manufacturer))

        return om

