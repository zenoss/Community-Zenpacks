################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVADeviceMap

HPEVADeviceMap maps HPEVA_StorageSystem class to hw and
os products.

$Id: HPEVADeviceMap.py,v 1.0 2010/03/10 13:05:00 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap,\
                                                                    MultiArgs

class HPEVADeviceMap(WBEMPlugin):
    """HPEVADeviceMap maps HPEVA_StorageSystem class to hw and
       os products.
    """

    maptype = "HPEVADeviceMap"
    modname = "ZenPacks.community.HPEVAMon.HPEVADevice" 
    deviceProperties = WBEMPlugin.deviceProperties + ('snmpSysName',)

    def queries(self, device):
	keybindings = {}
        sysname = getattr(device, "snmpSysName", None)
	if sysname:
	    keybindings = {
	        "HPEVA_StorageSystem":
		    {
		    "CreationClassName": "HPEVA_StorageSystem",
		    "Name": sysname,
		    },
	        "HPEVA_StorageControllerChassis":
		    {
		    "CreationClassName": "HPEVA_StorageControllerChassis",
		    "Tag":"%s.\Hardware\Controller Enclosure\Controller 1"%sysname,
		    },
		}

        return {
            "HPEVA_StorageSystem":
                (
                "HPEVA_StorageSystem",
		keybindings.get("HPEVA_StorageSystem", None),
                "root/eva",
                    {
		    "Comment":"comments",
		    "Description":"snmpDescr",
		    "ElementName":'_deviceName',
                    "Model":"setHWProductKey",
		    "Name":"snmpSysName",
		    "TotalStorageSpace":"_totalMemory",
                    },
                ),
            "HPEVA_StorageControllerChassis":
                (
                "HPEVA_StorageControllerChassis",
		keybindings.get("HPEVA_StorageControllerChassis", None),
                "root/eva",
                    {
		    "SerialNumber":"setHWSerialNumber",
		    "Version":"setOSProductKey",
                    },
                ),
            }


    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
	try:
	    cs = results["HPEVA_StorageSystem"][0]
            if not cs: return
	    cs.update(results["HPEVA_StorageControllerChassis"][0])
            maps = []
            om = self.objectMap(cs)
            om.snmpLocation = ""
            om.snmpOid = ""
	    if om.setHWProductKey == 'HSV300': om.setHWProductKey = 'EVA4400'
	    elif om.setHWProductKey == 'HSV400': om.setHWProductKey = 'EVA6400'
	    elif om.setHWProductKey == 'HSV450': om.setHWProductKey = 'EVA8400'
	    om.setHWProductKey = MultiArgs(om.setHWProductKey, "HP")
	    om.setOSProductKey = MultiArgs(om.setOSProductKey, "HP")
            maps.append(om)
	except:
	    raise
            log.warning("processing error")
	    return
        return maps

