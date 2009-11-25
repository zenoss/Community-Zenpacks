######################################################################
#
# Pdu7930Device modeler plugin
#
######################################################################

__doc__="""Pdu7930Device

PduOutletDevice maps Outlets and states to connected Devices

$Id: $"""

__version__ = '$Revision: $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class PduOutletDevice(SnmpPlugin):

    relname = "PduOutlet7930"
    modname = "ZenPacks.Iwillfearnoevil.Powernet7930.PduOutlet7930"
#    compname not needed as PduOutlet is a relationship on object class PduOutlet 
#    which is a direct child of Device"
#    compname = ""

    basecolumns = {
               '.1': 'OutletNumber',
               '.3': 'DeviceControlled',
             }

    statuscolumns = {
               '.3': 'Status',
             }

# snmpGetTableMaps gets tabular data

    snmpGetTableMaps = (
        # Main information on the Outlets
        GetTableMap('OutletDetails', '.1.3.6.1.4.1.318.1.1.4.5.2.1', basecolumns),
        # Attempt to get port status this hopefully will be split into an array
        GetTableMap('OutletState', '.1.3.6.1.4.1.318.1.1.4.4.2.1', statuscolumns),
    )
	   
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        #Collect Outlet status and details
        getdata, tabledata = results
        
# Uncomment next 2 lines for debugging when modeling
        log.warn( "Get Data= %s", getdata )
        log.warn( "Table Data= %s", tabledata )
        BaseTable = tabledata.get("OutletDetails")

# If no data returned then simply return
        if not BaseTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", getdata )
            log.warn( "Columns= %s", self.basecolumns )
            return


        rm = self.relMap()
        for oid, data in BaseTable.items():
            om = self.objectMap(data)
            om.id = self.prepId("OutletNumber_" + str(om.OutletNumber) + "_DeviceControlled_" + str(om.DeviceControlled))

# For lots of debugging, uncomment next 2 lines
            for key,value in om.__dict__.items():
               log.warn("om key =  %s, om value = %s", key,value)
            rm.append(om)
        return rm

