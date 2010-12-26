################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageProcessorCardMap

HPEVAStorageProcessorCardMap maps HPEVA_StorageProcessorCard class to
HPEVAStorageProcessorCard class.

$Id: HPEVA_StorageProcessorCardMap.py,v 1.1 2010/10/12 17:49:46 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class HPEVAStorageProcessorCardMap(WBEMPlugin):
    """Map HPEVA_StorageProcessorCard class to StorageProcessorCard"""

    maptype = "HPEVAStorageProcessorCardMap"
    modname = "ZenPacks.community.HPEVAMon.HPEVAStorageProcessorCard"
    relname = "cards"
    compname = "hw"
    deviceProperties = WBEMPlugin.deviceProperties + ('snmpSysName',)

    tables = {
            "HPEVA_StorageProcessorCard":
                (
                "HPEVA_StorageProcessorCard",
                None,
                "root/eva",
                    {
                    "Tag":"snmpindex",
                    "Caption":"caption",
                    "FirmwareVersion":"FWRev",
                    "Model":"setProductKey",
                    "Name":"id",
                    "SerialNumber":"serialNumber",
                    },
                ),
            }


    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        instances = results["HPEVA_StorageProcessorCard"]
        if not instances: return
        rm = self.relMap()
        sysname = getattr(device, "snmpSysName", None) or device.id
        for instance in instances:
            if not instance["id"].startswith(sysname): continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                om.slot = om.caption[-1]
                om.setProductKey = MultiArgs(om.setProductKey, "HP")
            except AttributeError:
                continue
            rm.append(om)
        return rm
