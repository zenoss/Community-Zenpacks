################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageDiskEnclosureMap

HPEVAStorageDiskEnclosureMap maps HPEVA_StorageDiskEnclosure class to
HPEVAStorageDiskEnclosure class.

$Id: HPEVA_StorageDiskEnclosureMap.py,v 1.3 2010/10/12 17:48:13 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class HPEVAStorageDiskEnclosureMap(WBEMPlugin):
    """Map HPEVA_StorageDiskEnclosure class to Storage Enclosure"""

    maptype = "HPEVAStorageDiskEnclosureMap"
    modname = "ZenPacks.community.HPEVAMon.HPEVAStorageDiskEnclosure"
    relname = "enclosures"
    compname = "hw"
    deviceProperties = WBEMPlugin.deviceProperties + ('snmpSysName',)

    tables = {
            "HPEVA_StorageDiskEnclosure":
                (
                "HPEVA_StorageDiskEnclosure",
                None,
                "root/eva",
                    {
                    "__path":"snmpindex",
                    "Caption":"id",
                    "Manufacturer":"_manuf",
                    "Model":"_model",
                    "Name":"_sname",
                    },
                ),
            "HPEVA_StorageSystem":
                (
                "HPEVA_StorageSystem",
                None,
                "root/eva",
                    {
                    "Model":"sysmodel",
                    "Name":"_sname",
                    },
                ),
            }

    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        sysmodels = {}
        instances = results.get("HPEVA_StorageSystem", [])
        for instance in instances:
            sysmodels[instance['_sname']] = instance['sysmodel']
        instances = results.get("HPEVA_StorageDiskEnclosure", None)
        if not instances: return
        rm = self.relMap()
        sysname = getattr(device, 'snmpSysName', None) or device.id
        for instance in instances:
            if instance["_sname"] != sysname: continue
            sysmodel = sysmodels.get(sysname, 'Unknown')
            om = self.objectMap(instance)
            om.id = self.prepId(om.id.split()[-1])
            try:
                if sysmodel in ['HSV300', 'HSV400', 'HSV450']:
                    om._model = 'M6412A'
                    om.enclosureLayout = '1 4 7 10,2 5 8 11,3 6 9 12'
                    om.hLayout = True
                elif sysmodel in ['HSV200-B', 'HSV210-B', 'HSV200B', 'HSV210B']:
                    om._model = 'M5314C'
                    om.enclosureLayout = '1 2 3 4 5 6 7 8 9 10 11 12 13 14'
                    om.hLayout = False
                else:
                    om._model = 'M5314A'
                    om.enclosureLayout = '1 2 3 4 5 6 7 8 9 10 11 12 13 14'
                    om.hLayout = False
                if om._model: om.setProductKey = MultiArgs(om._model, 'HP')
            except AttributeError:
                continue
            rm.append(om)
        return rm
