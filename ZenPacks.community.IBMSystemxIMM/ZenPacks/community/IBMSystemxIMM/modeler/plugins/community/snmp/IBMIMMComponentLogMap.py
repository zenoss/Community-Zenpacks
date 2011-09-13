# ==============================================================================
# IBMIMMComponentLogMap modeler plugin
#
# Zenoss community Zenpack for IBM SystemX Integrated Management Module
# version: 0.3
#
# (C) Copyright IBM Corp. 2011. All Rights Reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ==============================================================================

__doc__="""IBMIMMComponentLogMap maps chassis component VPD entries associated with an IMM"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "0.3.0"

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class IBMIMMComponentLogMap(SnmpPlugin):

    relname = "IMMCOMPLOG"
    modname = "ZenPacks.community.IBMSystemxIMM.IMMComponentLog"
    
    columns = {
               '.1': 'componentLevelVpdTrackingIndex',
               '.2': 'componentLevelVpdTrackingFruNumber',
               '.3': 'componentLevelVpdTrackingFruName',
               '.4': 'componentLevelVpdTrackingSerialNumber',
               '.5': 'componentLevelVpdTrackingManufacturingId',
               '.6': 'componentLevelVpdTrackingAction',
               '.7': 'componentLevelVpdTrackingTimestamp',
              }

    # snmpGetTableMaps gets tabular data
    snmpGetTableMaps = (
        # Chassis component VPD table
        GetTableMap('systemComponentLevelVpdTrackingEntry', '.1.3.6.1.4.1.2.3.51.3.1.5.18.1', columns),
    )
	   
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        # Collect the data from device
        getdata, tabledata = results
        
        # Debug: print data retrieved from device.
        log.warn( "Get data = %s", getdata )
        log.warn( "Table data = %s", tabledata )

        VpdTable = tabledata.get("systemComponentLevelVpdTrackingEntry")

        # If no data retrieved return nothing.
        if not VpdTable:
            log.warn( 'No data collected from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data = %s", getdata )
            log.warn( "Columns = %s", self.columns )
            return

        rm = self.relMap()
	   
        for oid, data in VpdTable.items():
            om = self.objectMap(data)
            om.id = self.prepId(om.componentLevelVpdTrackingFruName)
            om.componentLevelVpdTrackingIndex = int(om.componentLevelVpdTrackingIndex)

            # Debug: print values of object map.
#           for key,value in om.__dict__.items():
#              log.warn("om key=value: %s = %s", key,value)
	    
            rm.append(om) 
        return rm
