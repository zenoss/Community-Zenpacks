##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 15th, 2011
# Revised:
#
# JuniperDevice modler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperDeviceMap

Gather information from Juniper devices.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
import re

class JuniperDeviceMap(SnmpPlugin):
    maptype = "JuniperDeviceMap"

# Get OSProductKey from Host Resources SoftwareInstalled table - .2 index
# jnxBoxRevision ( .1.3.6.1.4.1.2636.3.1.4.0 ) is usually null 
    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2636.3.1.2.0': 'setHWProductKey',
        '.1.3.6.1.4.1.2636.3.1.4.0': '_modelNumber',
        '.1.3.6.1.4.1.2636.3.1.3.0': 'setHWSerialNumber',
        '.1.3.6.1.2.1.25.6.3.1.2.2': 'setOSProductKey',
        '.1.3.6.1.4.1.2636.3.1.16.0': 'memoryUsedPercent',
        '.1.3.6.1.4.1.2636.3.58.1.2.1.1.0': 'psuAvailable',

         })

    def condition(self, device, log):
        """only for boxes with proper object id
        """
        return device.snmpOid.startswith(".1.3.6.1.4.1.2636")


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        om = self.objectMap(getdata)
        manufacturer = "Juniper Networks, Inc."
        om.setHWProductKey = om.setHWProductKey + ' ' + om._modelNumber
        om.setHWProductKey = MultiArgs(om.setHWProductKey, manufacturer)
#        log.debug("HWProductKey=%s Manufacturer = %s" % (om.setHWProductKey, manufacturer))
        om.setOSProductKey = MultiArgs(om.setOSProductKey, manufacturer)
#        log.debug("OSProductKey=%s Manufacturer = %s" % (om.setOSProductKey, manufacturer))
#        log.debug("Memory used %s psu available = %s" % (om.memoryUsedPercent, om.psuAvailable))

        return om

