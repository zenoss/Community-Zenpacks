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

$Id: HPEVADeviceMap.py,v 1.5 2010/09/16 08:07:40 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]


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
#                    "SerialNumber":"setHWSerialNumber",
                    "Tag":"_tag",
                    "Version":"setOSProductKey",
                    },
                ),
            }

    def iloInterface(self, manageIp):
        om = ObjectMap({}, compname = "os",
                        modname = "Products.ZenModel.IpInterface")
        om.id = self.prepId("iLO Network Interface")
        om.title = om.id
        om.interfaceName = om.id
        om.type = "ethernetCsmacd"
        om.speed = 100000000
        om.mtu = 1500
        om.ifindex = "1"
        om.adminStatus = 1
        om.operStatus = 1
        om.monitor = False
        om.setIpAddresses = [manageIp, ]
        return RelationshipMap(relname = "interfaces", compname = "os",
                               modname = "Products.ZenModel.IpInterface",
                               objmaps = [om,])


    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        try:
            sysname = getattr(device, "snmpSysName", None)
            for cs in results.get("HPEVA_StorageControllerChassis", []):
                if not sysname and cs["_tag"].startswith(device.id): break
            if not cs: return
            for instance in results.get("HPEVA_StorageSystem", []):
                if not cs["_tag"].startswith(instance["snmpSysName"]): continue
                cs.update(instance)
                break
            maps = []
            om = self.objectMap(cs)
#            om.snmpLocation = ""
#            om.snmpOid = ""
            if om.setHWProductKey == 'HSV100': om.setHWProductKey = 'EVA3000'
            elif om.setHWProductKey == 'HSV110': om.setHWProductKey = 'EVA5000'
            elif om.setHWProductKey == 'HSV200': om.setHWProductKey = 'EVA6000'
            elif om.setHWProductKey == 'HSV200-B': om.setHWProductKey = 'EVA6100'
            elif om.setHWProductKey == 'HSV210': om.setHWProductKey = 'EVA8000'
            elif om.setHWProductKey == 'HSV210-B': om.setHWProductKey = 'EVA8100'
            elif om.setHWProductKey == 'HSV300': om.setHWProductKey = 'EVA4400'
            elif om.setHWProductKey == 'HSV400': om.setHWProductKey = 'EVA6400'
            elif om.setHWProductKey == 'HSV450': om.setHWProductKey = 'EVA8400'
            om.setHWProductKey = MultiArgs(om.setHWProductKey, "HP")
            om.setOSProductKey = MultiArgs(om.setOSProductKey, "HP")
            maps.append(om)
            if device.manageIp: maps.append(self.iloInterface(device.manageIp))
        except:
            log.warning("processing error")
            return
        return maps
