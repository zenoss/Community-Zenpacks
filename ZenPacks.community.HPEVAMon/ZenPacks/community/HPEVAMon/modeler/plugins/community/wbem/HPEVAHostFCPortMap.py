################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAHostFCPortMap

HPEVAHostFCPortMap maps HPEVA_HostFCPort class to
HPEVAHostFCPort class.

$Id: HPEVA_HostFCPortMap.py,v 1.0 2010/05/07 16:29:33 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class HPEVAHostFCPortMap(WBEMPlugin):
    """Map HPEVA_HostFCPort class to HostFCPort"""

    maptype = "HPEVAHostFCPortMap"
    modname = "ZenPacks.community.HPEVAMon.HPEVAHostFCPort"
    relname = "fcports"
    compname = "hw"
    deviceProperties = WBEMPlugin.deviceProperties + ('snmpSysName',)

    tables = {
            "HPEVA_HostFCPort":
                (
                "CIM_FCPort",
                None,
                "root/eva",
                    {
                    "__path":"snmpindex",
                    "ActiveFC4Types":"fc4Types",
                    "CreationClassName":"_ccn",
                    "Description":"description",
                    "DeviceID":"id",
                    "Caption":"interfaceName",
                    "FullDuplex":"fullDuplex",
                    "LinkTechnology":"linkTechnology",
                    "NetworkAddresses":"networkAddresses",
                    "PermanentAddress":"wwn",
                    "PortType":"type",
                    "Speed":"speed",
                    "SupportedMaximumTransmissionUnit":"mtu",
                    "SystemName":"setController",
                    },
                ),
            }

    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        instances = results["HPEVA_HostFCPort"]
        if not instances: return
        rm = self.relMap()
        sysname = getattr(device, "snmpSysName", 'None')
        for instance in instances:
            if not instance["setController"].startswith(sysname): continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                if om._ccn == 'HPEVA_DiskFCPort':
                    self.modname = "ZenPacks.community.HPEVAMon.HPEVADiskFCPort"
                if om.setController: om.setController = om.setController.strip()
                if om.interfaceName:om.interfaceName=om.interfaceName.split()[-1]
            except AttributeError:
                continue
            rm.append(om)
        return rm
