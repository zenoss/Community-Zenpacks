################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStoragePoolMap

HPEVAStoragePoolMap maps HPEVA_StoragePool class to
HPEVAStoragePool class.

$Id: HPEVA_StoragePoolMap.py,v 1.1 2010/05/14 19:31:17 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin

class HPEVAStoragePoolMap(WBEMPlugin):
    """Map HPEVA_StoragePool class to StoragePool"""

    maptype = "HPEVAStoragePoolMap"
    modname = "ZenPacks.community.HPEVAMon.HPEVAStoragePool"
    relname = "storagepools"
    compname = "os"
    deviceProperties = WBEMPlugin.deviceProperties + ('snmpSysName',)

    tables = {
            "HPEVA_StoragePool":
                (
                "HPEVA_StoragePool",
                None,
                "root/eva",
                    {
                    "__path":"snmpindex",
                    "ActualDiskFailureProtectionLevel":"protLevel",
                    "DiskGroupType":"diskGroupType",
                    "DiskType":"diskType",
                    "InstanceID":"id",
                    "Name":"caption",
                    "OccupancyAlarmLevel":"threshold",
                    "TotalDisks":"totalDisks",
                    "TotalManagedSpace":"totalManagedSpace",
                    },
                ),
            }

    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        instances = results["HPEVA_StoragePool"]
        if not instances: return
        rm = self.relMap()
        sysname = getattr(device, "snmpSysName", 'None')
        for instance in instances:
            if not instance["id"].startswith(sysname): continue
            if instance["id"].endswith('.Allocated Disks'): continue
            if instance["id"].endswith('.Ungrouped Disks'): continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                if type(om.threshold) is not int: om.threshold = 90
            except AttributeError:
                continue
            rm.append(om)
        return rm
