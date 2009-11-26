######################################################################
#
# PduOutletDevice modeler plugin
#
######################################################################

__doc__="""PduOutletDevice

PduOutletDevice maps Outlets and states to connected Devices

$Id: $"""

__version__ = '$Revision: $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class PduOutletDevice(SnmpPlugin):

    relname = "PduOutlet"
    modname = "ZenPacks.speakeasy.Powernet9225.PduOutlet"
#    compname not needed as PduOutlet is a relationship on object class Pdu9225 
#    which is a direct child of Device"
#    compname = ""

    basecolumns = {
               '.2': 'OutletController',
               '.3': 'OutletNumber',
               '.4': 'DeviceControlled',
               '.5': 'State',

             }

# snmpGetTableMaps gets tabular data

    snmpGetTableMaps = (
        # Main information on the Outlets
        GetTableMap('OutletDetails', '.1.3.6.1.4.1.318.1.1.6.7.1.1', basecolumns),
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
            om.id = self.prepId("OutletController_" + str(om.OutletController) + "_OutletNumber_" + str(om.OutletNumber) + "_DeviceControlled_" + str(om.DeviceControlled))

# For lots of debugging, uncomment next 2 lines
#            for key,value in om.__dict__.items():
#               log.warn("om key =  %s, om value = %s", key,value)
            rm.append(om)
        return rm

