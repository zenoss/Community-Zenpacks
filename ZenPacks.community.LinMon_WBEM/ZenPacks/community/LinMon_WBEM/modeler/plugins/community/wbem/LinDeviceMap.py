################################################################################
#
# This program is part of the LinMon_WBEM Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""LinDeviceMap

LinDeviceMap maps mib elements from cmpi-base classes to get hw and os products.

$Id: LinDeviceMap.py,v 1.0 2009/08/02 01:11:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class LinDeviceMap(WBEMPlugin):
    """Map mib elements from cmpi-base Classes to get hw and os products.
    """

    maptype = "LinDeviceMap" 

    def queries(self):
        return {
            "Linux_ComputerSystem":
                (
                "linux_ComputerSystem",
                None,
                "root/cimv2",
                None,
                ),
            "Linux_OperatingSystem":
                (
                "linux_OperatingSystem",
                None,
                "root/cimv2",
                None,
                ),
            }


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        Linux_CS = results['Linux_ComputerSystem'][0]
        Linux_OS = results['Linux_OperatingSystem'][0]
        maps = []
        om = self.objectMap()
        om.snmpDescr = Linux_CS['IdentifyingDescriptions']
        om.snmpContact = Linux_CS['PrimaryOwnerContact']
        om.snmpSysName = Linux_CS['Name']
        om.snmpLocation = ''
        om.snmpOid = ''
        om.setOSProductKey = Linux_OS['Version']
        maps.append(om)
#        om.setHWProductKey = MultiArgs(name, manuf)
#        om.setHWSerialNumber = sn
        maps.append(ObjectMap({"totalMemory":
                                    Linux_OS['TotalVisibleMemorySize'] * 1024},
                                                                compname="hw"))
        maps.append(ObjectMap({"totalSwap":
                                    Linux_OS['SizeStoredInPagingFiles'] * 1024},
                                                                compname="os"))
        return maps

