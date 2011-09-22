# ==============================================================================
# IBMIMMCpuVpdMap modeler plugin
#
# Zenoss community Zenpack for IBM SystemX Integrated Management Module
# version: 1.0
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

__doc__="""IBMIMMCpuVpdMap maps CPU VPD entries associated with an IMM"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "1.0.0"

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class IBMIMMCpuVpdMap(SnmpPlugin):

    relname = "IMMCPUVPD"
    modname = "ZenPacks.community.IBMSystemxIMM.IMMCpuVpd"

    columns = {
               '.1':  'cpuVpdIndex',
               '.2':  'cpuVpdDescription',
               '.3':  'cpuVpdSpeed',
               '.4':  'cpuVpdIdentifier',
               '.5':  'cpuVpdType',
               '.6':  'cpuVpdFamily',
               '.7':  'cpuVpdCores',
               '.8':  'cpuVpdThreads',
               '.9':  'cpuVpdVoltage',
               '.10': 'cpuVpdDataWidth',
              }

    # snmpGetTableMaps gets tabular data
    snmpGetTableMaps = (
        # System CPU VPD table
        GetTableMap('systemCPUVpdEntry', '.1.3.6.1.4.1.2.3.51.3.1.5.20.1', columns),
    )
	   
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        # Collect the data from device
        getdata, tabledata = results
        
        # Debug: print data retrieved from device.
        log.debug( "Get data = %s", getdata )
        log.debug( "Table data = %s", tabledata )

        VpdTable = tabledata.get("systemCPUVpdEntry")

        # If no data retrieved return nothing.
        if not VpdTable:
            log.warn( 'No data collected from %s for the %s plugin', device.id, self.name() )
            log.debug( "Data = %s", getdata )
            log.debug( "Columns = %s", self.columns )
            return

        rm = self.relMap()
	   
        for oid, data in VpdTable.items():
            om = self.objectMap(data)
            om.id = self.prepId(om.cpuVpdDescription)
            om.cpuVpdIndex = int(om.cpuVpdIndex)

            # Debug: print values of object map.
#           for key,value in om.__dict__.items():
#              log.warn("om key=value: %s = %s", key,value)
	    
            rm.append(om) 
        return rm
