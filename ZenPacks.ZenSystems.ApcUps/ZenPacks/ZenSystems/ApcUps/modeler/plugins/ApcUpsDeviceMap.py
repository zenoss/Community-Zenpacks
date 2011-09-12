##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 28th, 2011
# Revised:
#
# ApcUpsDevice modler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """ApcUpsDeviceMap

Gather information from APC UPS devices.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
import re

class ApcUpsDeviceMap(SnmpPlugin):
    maptype = "ApcUpsDeviceMap"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.318.1.1.1.1.1.1.0': 'setHWProductKey',
        '.1.3.6.1.4.1.318.1.1.1.1.2.1.0': 'setOSProductKey',
        '.1.3.6.1.4.1.318.1.1.1.1.2.3.0': 'setHWSerialNumber',
        '.1.3.6.1.4.1.318.1.1.1.2.2.5.0': 'numBatteryPacks',
        '.1.3.6.1.4.1.318.1.1.1.2.2.6.0': 'numBadBatteryPacks',
        '.1.3.6.1.4.1.318.1.1.1.4.1.1.0': 'basicOutputStatus',
         })

    def condition(self, device, log):
        """only for boxes with proper object id
        """
        return device.snmpOid.startswith(".1.3.6.1.4.1.318.1.3.2")


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        om = self.objectMap(getdata)
        manufacturer = "American Power Conversion Corp."
        om.setHWProductKey = MultiArgs(om.setHWProductKey, manufacturer)
#        log.debug("HWProductKey=%s Manufacturer = %s" % (om.setHWProductKey, manufacturer))
        om.setOSProductKey = MultiArgs(om.setOSProductKey, manufacturer)
#        log.debug("OSProductKey=%s Manufacturer = %s" % (om.setOSProductKey, manufacturer))
        if (om.basicOutputStatus < 1 or om.basicOutputStatus > 12):
            om.basicOutputStatus = 1
        index = om.basicOutputStatus
        om.basicOutputStatusText = self.basicOutputStatusMap[index]


        return om

    basicOutputStatusMap = { 1: 'Unknown',
                                  2: 'onLine',
                                  3: 'onBattery',
                                  4: 'onSmartBoost',
                                  5: 'timedSleeping',
                                  6: 'softwareBypass',
                                  7: 'off',
                                  8: 'rebooting',
                                  9: 'switchedBypass',
                                  10: 'hardwareFailureBypass',
                                  11: 'sleepingUntilPowerReturn',
                                  12: 'onSmartTrim',
                                }

