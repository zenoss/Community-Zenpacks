######################################################################
#
# BridgeInterfaceMib modeler plugin
#
######################################################################

__doc__="""BridgeInterfaceMib

BridgeInterfaceMib maps interfaces on a switch supporting the Bridge MIB

$Id: $"""

__version__ = '$Revision: $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class BridgeInterfaceMib(SnmpPlugin):

    relname = "BridgeInt"
    modname = "ZenPacks.skills1st.bridge.BridgeInterface"
#    compname not needed as BridgeInt is a relationship on object class BridgeDevice 
#    which is a direct child of Device"
#    compname = ""
    
    # New classification stuff uses wait to help it determine what class a
    # device should be in. Higher weight pushes the device to towards the 
    # class were this plugin is defined.
    weight = 4
    
    basecolumns = {
               '.1': 'BasePort',
               '.2': 'BasePortIfIndex',
             }

    portcolumns = {
               '.1': 'RemoteAddress',
               '.2': 'Port',
               '.3': 'PortStatus',
             }

# snmpGetTableMaps gets tabular data

    snmpGetTableMaps = (
        # Physical Port Forwarding Table
        GetTableMap('dot1dBasePortEntry', '.1.3.6.1.2.1.17.1.4.1', basecolumns),

        # Physical Port Forwarding Table
        GetTableMap('dot1dTpFdbEntry', '.1.3.6.1.2.1.17.4.3.1', portcolumns),
    )

	   
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        #Collect Physical Port Forwarding Table
        getdata, tabledata = results
        
# Uncomment next 2 lines for debugging when modeling
        log.warn( "Get Data= %s", getdata )
        log.warn( "Table Data= %s", tabledata )

        BaseTable = tabledata.get("dot1dBasePortEntry")

# If no data returned then simply return
        if not BaseTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", getdata )
            log.warn( "Columns= %s", self.basecolumns )
            return

        PortTable = tabledata.get("dot1dTpFdbEntry")

# If no data returned then simply return
        if not PortTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", getdata )
            log.warn( "Columns= %s", self.portcolumns )
            return

        rm = self.relMap()
        
        for oid, data in PortTable.items():
#
# oid for the Bridge MIB is dotted decimal representation of remote MAC address!
# However, the port number is used as the oid index into most of the other useful tables
#  eg. Port 13 = slot 1 on 2900; port 22 = slot 9
# Hence, set snmpindex to port
#
# Note that the RemoteAddress MAC field is raw hex so use asmac function to convert
#   to a string that displays sensibly
#
# dot1dBasePortIfIndex provides a link between port numbers on the switch from the BRIDGE
#   MIB and the interface table for standard MIB-2 data (like interface description and
#   performance parameters).

            om = self.objectMap(data)
            om.RemoteAddress = self.asmac(om.RemoteAddress)
            om.snmpindex = int(om.Port)
# The BasePortIfIndex is found from the BaseTable where the Port number from
# dot1dTpFdbEntry table matches the Port number from the dot1dBasePortEntry


            om.PortIfIndex = -1
            for boid,bdata in BaseTable.items():
               if bdata['BasePort'] == om.Port:
                   om.PortIfIndex = bdata['BasePortIfIndex'] 

# prepId function ensures that results are all unique - will add _1, _2 etc to achieve this
            om.id = self.prepId("%s_%s" % (om.Port, om.RemoteAddress))

# For lots of debugging, uncomment next 2 lines
#            for key,value in om.__dict__.items():
#               log.warn("om key =  %s, om value = %s", key,value)
	    
            rm.append(om) 
        return rm


