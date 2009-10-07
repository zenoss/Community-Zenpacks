######################################################################
#
# BridgeDeviceMib modeler plugin
#
######################################################################

__doc__="""BridgeDeviceMib

BridgeDeviceMib gets number of ports and base MAC address for switch supporting Bridge MIB

$Id: $"""

__version__ = '$Revision: $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class BridgeDeviceMib(SnmpPlugin):

#    relname = "BridgeInt"
    modname = "ZenPacks.skills1st.bridge.BridgeDevice"
#    compname = "BridgeDevice"

# snmpGetMap gets scalar SNMP MIBs (single values)
#  Use .1.3.6.1.2.1.17.1.1 ( dot1dBaseBridgeAddress) to populate the Serial No
#  and 1.3.6.1.2.1.17.1.2 ( dot1dBaseNumPorts ) to populate the Hardware tag
#  setHWSerialNumber and setHWTag are standard methods on any Device

    snmpGetMap = GetMap({
        '.1.3.6.1.2.1.17.1.1.0' :  'setHWSerialNumber',
        '.1.3.6.1.2.1.17.1.2.0' :  'setHWTag',
        })

	   
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        #Collect Physical Port Forwarding Table
        getdata, tabledata = results
        
# Uncomment next 2 lines for debugging when modeling
        log.warn( "Get Data= %s", getdata )
        log.warn( "Table Data= %s", tabledata )
        om = self.objectMap(getdata)
        om.setHWSerialNumber = self.asmac(om.setHWSerialNumber)
        om.setHWTag = "Number of ports = " + str(om.setHWTag)
        return om

