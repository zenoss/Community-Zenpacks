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

$Id: HPEVA_StorageVolumeMap.py,v 1.3 2010/11/28 13:24:20 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin

import re
DTPAT=re.compile(r'SystemName="([A-Fa-f0-9]{16})",DeviceID="([A-Fa-f0-9]{40})".*InstanceID="(.{56})"')

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
                    "DiskGroupID":"setStoragePool",
                    "MirrorCache":"mirrorCache",
                    "VDiskType":"diskType",
                    "PreferredPath":"preferredPath",
                    "Name": "id",
                    "OnlineController":"_cntrl",
                    "RaidType":"raidType",
                    "ReadCachePolicy":"readCachePolicy",
                    "SystemName":"_sname",
                    "WriteCachePolicy":"writeCachePolicy",
                    "DeviceID":"_did",
                    },
                ),
            "HPEVA_OrderedMemberOfCollection":
                (
                "HPEVA_OrderedMemberOfCollection",
                None,
                "root/eva",
                    {
                    "__path":"path",
                    },
                ),
            }


    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpSysName","") or device.id.replace("-","")
        drgroups = {}
        for instance in results.get("HPEVA_OrderedMemberOfCollection", []):
            r = DTPAT.search(instance.get("path", ""))
            if not r: continue
            g = r.groups()
            if g[0] != sysname : continue
            drgroups[g[1]] = g[2]
        for instance in results.get("HPEVA_StorageVolume", []):
            if instance["_sname"] != sysname: continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId("%s.%s"%(om._sname, om.id))
                om.setStoragePool = "%s.%s"%(om._sname, om.setStoragePool)
                if om._did in drgroups: om.setDRGroup = drgroups[om._did]
            except AttributeError:
                continue
            rm.append(om)
        return rm
