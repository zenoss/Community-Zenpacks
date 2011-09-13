# ==============================================================================
# IBMIMMVoltMonMap modeler plugin
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

__doc__="""IBMIMMVoltMonMap maps Voltage monitoring entries associated with an IMM"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "0.3.0"

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class IBMIMMVoltMonMap(SnmpPlugin):

    relname = "IMMVOLTMON"
    modname = "ZenPacks.community.IBMSystemxIMM.IMMVoltMon"
    
    columns = {
               '.1': 'voltIndex',
               '.2': 'voltDescr',
               '.3': 'voltReading',
               '.4': 'voltNominalReading',
#              '.5': 'voltNonRecovLimitHigh',
               '.6': 'voltCritLimitHigh',
#              '.7': 'voltNonCritLimitHigh',
#              '.8': 'voltNonRecovLimitLow',
               '.9': 'voltCritLimitLow',
#              '.10': 'voltNonCritLimitLow',
              }
    # snmpGetTableMaps gets tabular data
    snmpGetTableMaps = (
        # Voltage monitor table
        GetTableMap('voltEntry', '.1.3.6.1.4.1.2.3.51.3.1.2.2.1', columns),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        # Collect the data from device
        getdata, tabledata = results

        # Debug: print data retrieved from device.
        log.warn( "Get data = %s", getdata )
        log.warn( "Table data = %s", tabledata )

        VpdTable = tabledata.get("voltEntry")

        # If no data retrieved return nothing.
        if not VpdTable:
            log.warn( 'No data collected from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data = %s", getdata )
            log.warn( "Columns = %s", self.columns )
            return

        rm = self.relMap()
	   
        for oid, data in VpdTable.items():
            om = self.objectMap(data)
            om.id = self.prepId(om.voltDescr)
            om.snmpindex = int(om.voltIndex)
#           om.voltIndex = int(om.voltIndex)
            om.voltReading = float(om.voltReading)/1000
            om.voltNominalReading = float(om.voltNominalReading)/1000
            om.voltCritLimitHigh = float(om.voltCritLimitHigh)/1000
            om.voltCritLimitLow = float(om.voltCritLimitLow)/1000

            # Debug: print values of object map.
#           for key,value in om.__dict__.items():
#              log.warn("om key=value: %s = %s", key,value)
	    
            rm.append(om) 
        return rm
