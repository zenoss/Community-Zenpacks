################################################################################
#
# This program is part of the WBEMPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""NewDeviceMap

DeviceMap maps CIM_ComputerSystem and CIM_OperationSystem classes to get hw and
os products.

$Id: NewDeviceMap.py,v 1.0 2010/02/17 23:30:15 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.EnterpriseOIDs import EnterpriseOIDs

class NewDeviceMap(WBEMPlugin):
    """
    Record basic hardware/software information based on the Linux_ComputerSystem
    and Linux_OperatingSystem.
    """

    maptype = "NewDeviceMap" 

    tables = {
            "Linux_BaseBoard":
                (
                "Linux_BaseBoard",
                None,
                "root/cimv2",
                    {
                    'Manufacturer':'_manuf',
                    'Model':'_model',
                    },
                ),
            "Linux_OperatingSystem":
                (
                "Linux_OperatingSystem",
                None,
                "root/cimv2",
                    {
                    'Version':'version',
                    },
                ),
            }


    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        try:
            cs = results['Linux_BaseBoard'][0]
            if not cs: return
            os = results['Linux_OperatingSystem'][0]
            if not os: return
            om = self.objectMap()
            if cs['_manuf'] not in EnterpriseOIDs.values():
                cs['_manuf'] = 'Unknown'
            om.setHWProductKey = MultiArgs(cs['_model'], cs['_manuf'])
            osmanuf = os['version'].split()[0]
            if osmanuf not in EnterpriseOIDs.values():
                osmanuf = 'Unknown'
            om.setOSProductKey = MultiArgs(os['version'], osmanuf)
        except:
            return
        return om

