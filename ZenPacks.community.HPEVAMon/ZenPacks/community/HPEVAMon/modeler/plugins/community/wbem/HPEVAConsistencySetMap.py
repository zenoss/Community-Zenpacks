################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAConsistencySetMap

HPEVAConsistencySetMap maps HPEVA_ConsistencySet class to
HPEVAConsistencySet class.

$Id: HPEVA_ConsistencySetMap.py,v 1.0 2010/11/28 21:27:31 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin

class HPEVAConsistencySetMap(WBEMPlugin):
    """Map HPEVA_ConsistencySet class to ConsistencySet"""

    maptype = "HPEVAConsistencySetMap"
    modname = "ZenPacks.community.HPEVAMon.HPEVAConsistencySet"
    relname = "drgroups"
    compname = "os"
    deviceProperties = WBEMPlugin.deviceProperties + ('snmpSysName',)

    tables = {
            "HPEVA_ConsistencySet":
                (
                "HPEVA_ConsistencySet",
                None,
                "root/eva",
                    {
                    "__path":"snmpindex",
                    "AsyncType":"_asyncType",
                    "drmlogdiskgroupid":"setStoragePool",
                    "ElementName":"caption",
                    "FailSafe":"failSafe",
                    "HostAccessMode":"hostAccessMode",
                    "InstanceID": "id",
                    "ParticipationType":"participationType",
                    "RemoteCellName":"remoteCellName",
                    "SuspendMode":"suspendMode",
                    "WriteMode":"writeMode",
                    },
                ),
            }


    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpSysName","") or device.id.replace("-","")
        for instance in results.get("HPEVA_ConsistencySet", []):
            if not instance["id"].startswith(sysname): continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                om.caption = om.caption.split('\\')[-1]
                om.setStoragePool = "%s.%s"%(sysname, om.setStoragePool)
                if om.writeMode == "asynchronous":
                    if om._asyncType in ["basic", "enhanced"]:
                        om.writeMode = "asynchronous (%s)"%om._asyncType
            except AttributeError:
                continue
            rm.append(om)
        return rm
