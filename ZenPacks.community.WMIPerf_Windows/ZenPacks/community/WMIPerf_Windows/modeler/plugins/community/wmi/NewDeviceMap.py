################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""NewDeviceMap

DeviceMap maps CIM_ComputerSystem and CIM_OperationSystem classes to get hw and
os products.

$Id: DeviceMap.py,v 1.0 2010/01/03 14:09:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.EnterpriseOIDs import EnterpriseOIDs

class NewDeviceMap(WMIPlugin):
    """
    Record basic hardware/software information based on the Win32_ComputerSystem
    and Win32_OperatingSystem.
    """

    maptype = "NewDeviceMap" 

    def queries(self):
        return {
            "Win32_ComputerSystem":
                (
                "Win32_ComputerSystem",
                None,
                "root/cimv2",
                    {
                    'Manufacturer':'_manuf',
                    'Model':'_model',
                    },
                ),
            "Win32_OperatingSystem":
                (
                "Win32_OperatingSystem",
                None,
                "root/cimv2",
                    {
                    'Name':'_name',
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
            om = self.objectMap()
            if cs['_manuf'] in EnterpriseOIDs.values():
                om.setHWProductKey = MultiArgs(cs['_model'], cs['_manuf'])
            else:
                om.setHWProductKey = MultiArgs(cs['_model'], 'Unknown')
            om.setOSProductKey=MultiArgs(os['_name'].split('|')[0],'Microsoft')
        except:
            return
        return om

