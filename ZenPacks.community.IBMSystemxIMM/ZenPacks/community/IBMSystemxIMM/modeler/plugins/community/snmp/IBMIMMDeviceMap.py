# ==============================================================================
# IBMIMMDeviceMap modeler plugin
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

__doc__="""IBMIMMDeviceMap gets data associated with the IMM at the device level"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "1.0.0"

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
        # Assuming the IMM firmware is always the first instance in immVpdTable.
        # If that turns out to be a bad assumption will need more logic here (i.e. like IBMIMMFwVpdMap).
        '.1.3.6.1.4.1.2.3.51.3.1.5.1.1.2.1' : 'immFirmwareVpdType',
        '.1.3.6.1.4.1.2.3.51.3.1.5.1.1.3.1' : 'immFirmwareVersionString',
        '.1.3.6.1.4.1.2.3.51.3.1.5.1.1.4.1' : 'immFirmwareReleaseDate',
        # Uncomment this if sysDescr will be used below.
#       '.1.3.6.1.2.1.1.1.0' : 'sysDescr',
        })

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        #Collect data
        getdata, tabledata = results
        
        # Debug: print data retrieved from device.
        log.debug( "Get data = %s", getdata )
        log.debug( "Table data = %s", tabledata )

        om = self.objectMap(getdata)

#       log.debug("MTM string length = %i", len(str(om.machineLevelVpdMachineModel)))
 
        # Expecting 7-char MTM here. If so, break into 4 char Machine Type + 3 char Model, 
        # hyphenate for readability. Otherwise leave unaltered.
        if len(str(om.machineLevelVpdMachineModel)) == 7:
            om.machineLevelVpdMachineModel = str(om.machineLevelVpdMachineModel)[:4] + '-' + str(om.machineLevelVpdMachineModel)[-3:]

        # Assemble the string to be used as "OS Model" below.
        immFirmwareString = om.immFirmwareVpdType + "-FW-" + om.immFirmwareVersionString + "-" + om.immFirmwareReleaseDate

        # Set values on Overview page
        # see: http://community.zenoss.org/docs/DOC-2350
        # setHWTag -> "Tag" field
        # setHWSerialNumber -> "Serial Number" field
        # setHWProductKey -> "Hardware Model", "Hardware Manufacturer"
        # setOSProductKey -> "OS Model", "OS Manufacturer"
        # comments -> "Comments" field
        # also: snmpContact, snmpSysName, snmpLocation, snmpUpTime

        om.setHWTag = str(om.machineLevelVpdMachineModel)
        om.setHWSerialNumber = str(om.machineLevelSerialNumber)

        # Test...
#       om.setHWProductKey = MultiArgs("Hardware Model", "Hardware Manufacturer")
#       om.setOSProductKey = MultiArgs("OS Model", "OS Manufacturer")

        om.setHWProductKey = MultiArgs(om.machineLevelProductName, "IBM")
#       om.setOSProductKey = MultiArgs("Integrated Management Module", "IBM")
        om.setOSProductKey = MultiArgs(immFirmwareString, "IBM")

        # 2nd field of sysDescr is hostname as set on Network Interfaces page in web UI.
        # Uncomment to add this data to Comment field.
#       om.comments = "IMM Hostname: " + str(om.sysDescr).split(' ')[1] + "\nSystem UUID: " + om.machineLevelUUID
    
        return om
