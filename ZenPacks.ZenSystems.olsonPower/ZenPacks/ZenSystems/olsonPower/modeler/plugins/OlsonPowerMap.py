##########################################################################
# Author:		Jane Curry,  jane.curry@skills-1st.co.uk
# Date:			January 24th, 2011
# Revised:
# 
# Modeler plugin for Olson Power Meters
# Delivers:		Hardware manufacturer & model
#			OS manufacturer & model
#			Serial No - actually "moduleName" - no real 
#				    serial no available with SNMP
#
##########################################################################


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

#import os
#import Globals
#from Products.ZenUtils.ZenScriptBase import ZenScriptBase
#from transaction import commit
#dmd = ZenScriptBase(connect=True).dmd

	
class OlsonPowerMap(SnmpPlugin):
    """Map mib elements from Olson device mib to get hw and os data.
    """

    maptype = "OlsonPowerMap" 

    snmpGetMap = GetMap({ 
        '.1.3.6.1.4.1.17933.1.1.1' : 'setHWProductKey',
        '.1.3.6.1.4.1.17933.1.1.2' : 'setOSProductKey',
        '.1.3.6.1.4.1.17933.1.1.3' : 'setHWSerialNumber',
         })
	
	
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        om = self.objectMap(getdata)
        om.setHWProductKey = MultiArgs(om.setHWProductKey, 'Olson')
        om.setOSProductKey = MultiArgs(om.setOSProductKey, 'Olson')

        return om
	
