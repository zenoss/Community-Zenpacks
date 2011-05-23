##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 28th, 2011
# Revised:
#
# ApcUpsBattery modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """ApcUpsBatteryMap

Gather table information for APC UPS batteries
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class ApcUpsBatteryMap(SnmpPlugin):
    """Map APC UPS Battery table to model."""
    maptype = "ApcUpsBatteryMap"
    modname = "ZenPacks.ZenSystems.ApcUps.ApcUpsBattery"
    relname = "ApcUpsBat"
    compname = ""

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.318.1.1.1.2.1.1.0': 'batteryStatus',
        '.1.3.6.1.4.1.318.1.1.1.2.1.2.0': 'timeOnBattery',
        '.1.3.6.1.4.1.318.1.1.1.2.1.3.0': 'batteryLastReplacementDate',
        '.1.3.6.1.4.1.318.1.1.1.2.2.4.0': 'batteryReplaceIndicator',
         })

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        if not getdata:
            log.warn(' No SNMP response from %s for the %s plugin ' % ( device.id, self.name ) )
            return

        om = self.objectMap(getdata)
# timeOnBattery is in timeticks (1/100 sec) so convert to minutes
        om.timeOnBattery = om.timeOnBattery / 6000
        om.id = "Battery"
        om.id = self.prepId(om.id)
# Transform battery status into a severity number via self.batteryStatusMap lookup
        if (om.batteryStatus < 1 or om.batteryStatus > 3):
            om.batteryStatus = 1
        index = om.batteryStatus
        om.batteryStatus = self.batteryStatusMap[index][0]
        om.batteryStatusText = self.batteryStatusMap[index][1]

# Transform batteryReplaceIndicator into a status string via self.batteryReplaceIndicatorMap lookup
        if (om.batteryReplaceIndicator < 1 or om.batteryReplaceIndicator > 2):
            om.batteryReplaceIndicator = 0
        index = om.batteryReplaceIndicator
        om.batteryReplaceIndicator = self.batteryReplaceIndicatorMap[index][0]
        om.batteryReplaceIndicatorText = self.batteryReplaceIndicatorMap[index][1]

# Need to set snmpindex to 0 to make component performance templates work
#
        om.snmpindex = '0'
# Uncomment next 2 lines for lots of debug info
#        for key,value in om.__dict__.items():
#            log.info('om key %s   om value %s ' % (key, value) )
        rm.append(om)
#        log.info('rm %s' % (rm) )
        return rm

    batteryStatusMap  =    { 1: ( 2, 'Status Unknown'),
                             2: ( 0, 'Status Normal'),
                             3: ( 5, 'Battery Low'),
                           }

    batteryReplaceIndicatorMap = { 0: ( 2, ' Status Unknown'),
                                   1: ( 0, 'OK'),
                                   2: ( 5, 'Battery needs replacing'),
                                 }



