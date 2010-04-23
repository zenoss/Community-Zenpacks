################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DeviceMap

DeviceMap maps CIM_ComputerSystem and CIM_OperationSystem classes to get hw and
os products.

$Id: DeviceMap.py,v 1.2 2010/04/23 07:41:12 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]


from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class DeviceMap(WMIPlugin):
    """DeviceMap maps CIM_ComputerSystem and CIM_OperationSystem classes to get hw and
       os products.
    """

    maptype = "DeviceMap" 

    tables = {
            "Win32_ComputerSystem":
                (
                "Win32_ComputerSystem",
                None,
                "root/cimv2",
                    {
                    'IdentifyingDescriptions':'snmpDescr',
                    'Manufacturer':'_manufacturer',
                    'Model':'_model',
                    'DNSHostName':'snmpSysName',
                    'PrimaryOwnerContact': 'snmpContact',
                    },
                ),
            "Win32_OperatingSystem":
                (
                "Win32_OperatingSystem",
                None,
                "root/cimv2",
                    {
                    'Name':'_name',
                    'TotalVisibleMemorySize':'totalMemory',
                    'SizeStoredInPagingFiles':'totalSwap',
                    },
                ),
            "Win32_SystemEnclosure":
                (
                "Win32_SystemEnclosure",
                None,
                "root/cimv2",
                    {
                    'SerialNumber':'sn',
                    },
                ),
            }


    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        try:
            cs = results['Win32_ComputerSystem'][0]
            if not cs: return
            os = results['Win32_OperatingSystem'][0]
            if not os: return
            sn = results.get('Win32_SystemEnclosure',({'sn':None},))[0]['sn']
            maps = []
            om = self.objectMap(cs)
            om.snmpLocation = ''
            om.snmpOid = ''
            om.setOSProductKey=MultiArgs(os['_name'].split('|')[0],'Microsoft')
            om.setHWProductKey = MultiArgs(cs['_model'], cs['_manufacturer'])
            if str(sn) != 'None': om.setHWSerialNumber = sn
            maps.append(om)
            maps.append(ObjectMap({"totalMemory": (os['totalMemory'] * 1024)},
                                                                compname="hw"))
            maps.append(ObjectMap({"totalSwap": (os['totalSwap'] * 1024)},
                                                                compname="os"))
        except:
            log.warning('processing error')
            return
        return maps

