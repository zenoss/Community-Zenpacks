################################################################################
#
# This program is part of the LinMon_WBEM Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DeviceMap

DeviceMap maps CIM_ComputerSystem and CIM_OperationSystem classes to get hw and
os products.

$Id: DeviceMap.py,v 1.0 2010/02/17 23:29:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.EnterpriseOIDs import EnterpriseOIDs

class DeviceMap(WBEMPlugin):
    """DeviceMap maps Linux_ComputerSystem and Linux_OperationSystem classes to
       get hw and os products.
    """

    maptype = "DeviceMap" 

    tables = {
            "Linux_BaseBoard":
                (
                "Linux_BaseBoard",
                None,
                "root/cimv2",
                    {
                    'Manufacturer':'_manuf',
                    'Model':'_model',
                    'SerialNumber':'serialNumber',
                    'Tag':'tag',
                    },
                ),
            "Linux_ComputerSystem":
                (
                "Linux_ComputerSystem",
                None,
                "root/cimv2",
                    {
                    'IdentifyingDescriptions':'snmpDescr',
                    'Name':'snmpSysName',
                    'PrimaryOwnerContact': 'snmpContact',
                    },
                ),
            "Linux_OperatingSystem":
                (
                "Linux_OperatingSystem",
                None,
                "root/cimv2",
                    {
                    'Version':'version',
                    'TotalVisibleMemorySize':'totalMemory',
                    'SizeStoredInPagingFiles':'totalSwap',
                    },
                ),
            }


    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        try:
            bb = results['Linux_BaseBoard'][0]
            if not bb: return
            cs = results['Linux_ComputerSystem'][0]
            if not cs: return
            os = results['Linux_OperatingSystem'][0]
            if not os: return
            maps = []
            om = self.objectMap(cs)
            om.snmpLocation = ''
            om.snmpOid = ''
            if bb['_manuf'] not in EnterpriseOIDs.values():
                bb['_manuf'] = 'Unknown'
            om.setHWProductKey = MultiArgs(bb['_model'], bb['_manuf'])
            osmanuf = os['version'].split()[0]
            if osmanuf not in EnterpriseOIDs.values():
                osmanuf = 'Unknown'
            om.setOSProductKey = MultiArgs(os['version'], osmanuf)
            maps.append(om)
            maps.append(ObjectMap({ "serialNumber": bb['serialNumber'],
                                    "tag": bb['tag'],
                                    "totalMemory": (os['totalMemory'] * 1024)},
                                                                compname="hw"))
            maps.append(ObjectMap({"totalSwap": (os['totalSwap'] * 1024)},
                                                                compname="os"))
        except:
            log.warning('processing error')
            return
        return maps

