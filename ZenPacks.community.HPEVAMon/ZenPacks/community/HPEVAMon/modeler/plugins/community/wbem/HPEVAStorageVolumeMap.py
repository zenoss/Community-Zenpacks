################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageVolumeMap

HPEVAStorageVolumeMap maps HPEVA_StorageVolume class to
HPEVAStorageVolume class.

$Id: HPEVA_StorageVolumeMap.py,v 1.1 2010/10/12 17:50:33 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin

class HPEVAStorageVolumeMap(WBEMPlugin):
    """Map HPEVA_StorageVolume class to StorageVolume"""

    maptype = "HPEVAStorageVolumeMap"
    modname = "ZenPacks.community.HPEVAMon.HPEVAStorageVolume"
    relname = "virtualdisks"
    compname = "os"
    deviceProperties = WBEMPlugin.deviceProperties + ('snmpSysName',)

    tables = {
            "HPEVA_StorageVolume":
                (
                "HPEVA_StorageVolume",
                None,
                "root/eva",
                    {
                    "__path":"snmpindex",
                    "Access":"accessType",
                    "Caption":"caption",
                    "BlockSize":"blockSize",
                    "DiskGroupID":"_dgid",
                    "MirrorCache":"mirrorCache",
                    "VDiskType":"diskType",
                    "PreferredPath":"preferredPath",
                    "Name": "id",
                    "OnlineController":"_cntrl",
                    "RaidType":"raidType",
                    "ReadCachePolicy":"readCachePolicy",
                    "SystemName":"_sname",
                    "WriteCachePolicy":"writeCachePolicy",
                    },
                ),
            }


    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        instances = results["HPEVA_StorageVolume"]
        if not instances: return
        rm = self.relMap()
        sysname = getattr(device, "snmpSysName", None) or device.id
        for instance in instances:
            if instance["_sname"] != sysname: continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId("%s.%s"%(om._sname, om.id))
                om.setStoragePool = "%s.%s"%(om._sname, om._dgid)
            except AttributeError:
                continue
            rm.append(om)
        return rm
