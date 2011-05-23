##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 7th, 2011
# Revised:
#
# ApcAtsDevice modler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """ApcAtsDeviceMap

Gather information from APC ATS devices.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
import re

class ApcAtsDeviceMap(SnmpPlugin):
    maptype = "ApcAtsDeviceMap"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.318.1.1.8.1.5.0': 'modelNumber',
        '.1.3.6.1.4.1.318.1.1.8.1.1.0': 'hardwareRev',
        '.1.3.6.1.4.1.318.1.1.8.1.2.0': 'setOSProductKey',
        '.1.3.6.1.4.1.318.1.1.8.1.6.0': 'setHWSerialNumber',
        '.1.3.6.1.4.1.318.1.1.8.5.1.2.0': 'statusSelectedSource',
        '.1.3.6.1.4.1.318.1.1.8.5.1.3.0': 'statusRedundancyState',
        '.1.3.6.1.4.1.318.1.1.8.5.1.12.0': 'statusSourceAStatus',
        '.1.3.6.1.4.1.318.1.1.8.5.1.13.0': 'statusSourceBStatus',
        '.1.3.6.1.4.1.318.1.1.8.5.1.14.0': 'statusPhaseSyncStatus',
         })

    def condition(self, device, log):
        """only for boxes with proper object id
        """
        return device.snmpOid.startswith(".1.3.6.1.4.1.318.1.3.11")


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        om = self.objectMap(getdata)
        manufacturer = "American Power Conversion Corp."
        om.setHWProductKey = om.modelNumber + ' ' + om.hardwareRev
        om.setHWProductKey = MultiArgs(om.setHWProductKey, manufacturer)
        log.debug("HWProductKey=%s Manufacturer = %s" % (om.setHWProductKey, manufacturer))
        om.setOSProductKey = MultiArgs(om.setOSProductKey, manufacturer)
        log.debug("OSProductKey=%s Manufacturer = %s" % (om.setOSProductKey, manufacturer))

        return om

