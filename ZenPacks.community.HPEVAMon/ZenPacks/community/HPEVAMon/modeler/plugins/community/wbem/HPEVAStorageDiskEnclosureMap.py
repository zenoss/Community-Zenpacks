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

$Id: HPEVA_StorageDiskEnclosureMap.py,v 1.1 2010/06/23 00:31:52 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


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
                    "Height":"_height",
                    "Manufacturer":"_manuf",
                    "Model":"_model",
                    "Name":"_sname",
                    },
                ),
            }

    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        instances = results["HPEVA_StorageDiskEnclosure"]
        if not instances: return
        rm = self.relMap()
        sysname = getattr(device, "snmpSysName", 'None')
        for instance in instances:
            if instance["_sname"] != sysname: continue
            om = self.objectMap(instance)
            om.id = self.prepId(om.id.split()[-1])
            try:
	        if om._height < 4:
		    om.enclosureLayout = '1 4 7 10,2 5 8 11,3 6 9 12'
		    om.hLayout = True
		else:
		    om.enclosureLayout = '1 2 3 4 5 6 7 8 9 10 11 12 13 14'
		    om.hLayout = False
                if not om._manuf: om._manuf = "Unknown"
                if om._model: om.setProductKey = MultiArgs(om._model, om._manuf)
            except AttributeError:
                continue
            rm.append(om)
        return rm
