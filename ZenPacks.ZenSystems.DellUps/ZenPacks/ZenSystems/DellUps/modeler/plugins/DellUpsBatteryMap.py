##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 8th, 2011
# Revised:
#
# DellUpsBattery modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """DellUpsBatteryMap

Gather table information for Dell UPS batteries
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class DellUpsBatteryMap(SnmpPlugin):
    """Map Dell UPS Battery table to model."""
    maptype = "DellUpsBatteryMap"
    modname = "ZenPacks.ZenSystems.DellUps.DellUpsBattery"
    relname = "DellUpsBat"
    compname = ""

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.674.10902.2.120.5.1.0': 'batteryABMStatus',
        '.1.3.6.1.4.1.674.10902.2.120.5.2.0': 'batteryTestStatus',
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
        om.id = "Battery"
        om.id = self.prepId(om.id)
# Transform ABM status into a severity number via self.batteryABMStatusMap lookup
        if (om.batteryABMStatus < 1 or om.batteryABMStatus > 5):
            om.batteryABMStatus = 0
        index = om.batteryABMStatus
        om.batteryABMStatus = self.batteryABMStatusMap[index][0]
        om.batteryABMStatusText = self.batteryABMStatusMap[index][1]

# Transform Test status into a status string via self.batteryTestStatusMap lookup
        batteryTestStatusNum = int(om.batteryTestStatus)
        if (batteryTestStatusNum < 1 or batteryTestStatusNum > 7):
            om.batteryTestStatus = "Unknown"
        else:
            om.batteryTestStatus = self.batteryTestStatusMap[batteryTestStatusNum]

# Need to set snmpindex to 0 to make component performance templates work
#
        om.snmpindex = '0'
# Uncomment next 2 lines for lots of debug info
#        for key,value in om.__dict__.items():
#            log.info('om key %s   om value %s ' % (key, value) )
        rm.append(om)
#        log.info('rm %s' % (rm) )
        return rm

    batteryABMStatusMap  = { 0: ( 3, 'ABM Unknown'),
                             1: ( 3, 'ABM Charging'),
                             2: ( 5, 'ABM discharging'),
                             3: ( 0, 'ABM floating'),
                             4: ( 2, 'ABM resting'),
                             5: ( 1, 'ABM off')
                           }

    batteryTestStatusMap = { 1: 'Done and Passed',
                             2: 'Done and Warning',
                             3: 'Done and Error',
                             4: 'Aborted',
                             5: 'In progress',
                             6: 'Not implemented',
                             7: 'Scheduled'
                           }



