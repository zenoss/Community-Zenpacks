################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVADiskDriveMap

HPEVADiskDriveMap maps HPEVA_DiskDrive class to HardDisk class.

$Id: HPEVA_DiskDriveMap.py,v 1.2 2010/10/15 20:50:33 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class HPEVADiskDriveMap(WBEMPlugin):
    """Map HPEVA_DiskDrive class to HardDisk"""

    maptype = "HPEVAHardDiskMap"
    modname = "ZenPacks.community.HPEVAMon.HPEVADiskDrive"
    relname = "harddisks"
    compname = "hw"
    deviceProperties = WBEMPlugin.deviceProperties + ('snmpSysName',)

    tables = {
            "HPEVA_DiskDrive":
                (
                "HPEVA_DiskDrive",
                None,
                "root/eva",
                    {
                    "DeviceID":"id",
                    "Caption":"bay",
                    "DiskType":"diskType",
                    "DriveType":"_diskType",
                    "FirmwareRevision":"FWRev",
                    "Manufacturer":"_manuf",
                    "MaxMediaSize":"size",
                    "Model":"_model",
                    "Name":"wwn",
                    "ShortName":"description",
                    "SystemName":"_sname",
                    },
                ),
            "HPEVA_DiskModule":
                (
                "HPEVA_DiskModule",
                None,
                "root/eva",
                    {
                    "DeviceID":"_id",
                    "HotSwappable":"hotPlug",
                    "SerialNumber":"serialNumber",
                    "Tag":"snmpindex",
                    },
                ),
            }

    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        diskModules = {}
        for instance in results.get("HPEVA_DiskModule", []):
            diskModules[instance['_id']] = instance
        sysname = getattr(device,"snmpSysName","") or device.id.replace("-","")
        for instance in results.get("HPEVA_DiskDrive", []):
            if instance["_sname"] != sysname: continue
            try:
                instance.update(diskModules.get(instance['id'], {}))
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                om.diskType = str('%s %s'%(om._diskType or '',
                                    om.diskType or 'Unknown')).replace('_', ' ')
                om.size = int(om.size) * 1000
                bay = om.bay.split(",", 2)
                om.setEnclosure = bay[0][6:]
                om.setStoragePool = bay[2][12:]
                om.bay = bay[1][10:]
                if om._model == 'HPQ': om._model = 'HP'
                om.setProductKey = MultiArgs(om._model, om._manuf)
            except AttributeError:
                raise
            rm.append(om)
        return rm
