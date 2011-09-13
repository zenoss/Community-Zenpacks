# ==============================================================================
# IBMIMMDeviceMap modeler plugin
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

__doc__="""IBMIMMDeviceMap gets data associated with the IMM at the device level"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "0.3.0"

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.plugins.DataMaps import ObjectMap

class IBMIMMDeviceMap(SnmpPlugin):

    relname = "IMMFWVPD"
    modname = "ZenPacks.community.IBMSystemxIMM.IMMDevice"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2.3.51.3.1.5.2.1.2.0' : 'machineLevelVpdMachineModel',
        '.1.3.6.1.4.1.2.3.51.3.1.5.2.1.3.0' : 'machineLevelSerialNumber',
        '.1.3.6.1.4.1.2.3.51.3.1.5.2.1.4.0' : 'machineLevelUUID',
        '.1.3.6.1.4.1.2.3.51.3.1.5.2.1.5.0' : 'machineLevelProductName',
        '.1.3.6.1.2.1.1.1.0' : 'sysDescr',
        })
   
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        #Collect data
        getdata, tabledata = results
        
        # Debug: print data retrieved from device.
        log.warn( "Get data = %s", getdata )
        log.warn( "Table data = %s", tabledata )

        om = self.objectMap(getdata)

        # Set values on Overview page
        # see: http://community.zenoss.org/docs/DOC-2350
        # setHWTag -> "Tag" field
        # setHWSerialNumber -> "Serial Number" field
        # setHWProductKey -> "Hardware Model", "Hardware Manufacturer"
        # setOSProductKey -> "OS Model", "OS Manufacturer"
        # comments -> "Comments" field
        # also: snmpContact, snmpSysName, snmpLocation, snmpUpTime

        om.setHWTag = str(om.machineLevelProductName)
        om.setHWSerialNumber = str(om.machineLevelSerialNumber)

        log.debug("MTM string length = %i", len(str(om.machineLevelVpdMachineModel)))
 
        # Expecting 7-char MTM here. If so, break into 4 char Machine Type + 3 char Model, 
        # hyphenate for readability. Otherwise leave unaltered.
        if len(str(om.machineLevelVpdMachineModel)) == 7:
            om.machineLevelVpdMachineModel = str(om.machineLevelVpdMachineModel)[:4] + '-' + str(om.machineLevelVpdMachineModel)[-3:]

        # Test...
#       om.setHWProductKey = MultiArgs("Hardware Model", "Hardware Manufacturer")
#       om.setOSProductKey = MultiArgs("OS Model", "OS Manufacturer")

        om.setHWProductKey = MultiArgs(om.machineLevelVpdMachineModel, "IBM")
        om.setOSProductKey = MultiArgs("Integrated Management Module", "IBM")

        # 2nd field of sysDescr is hostname as set on Network Interfaces page in web UI.
        om.comments = "IMM Hostname: " + str(om.sysDescr).split(' ')[1] + "\nSystem UUID: " + om.machineLevelUUID
    
        return om
