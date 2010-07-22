################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DiskDriveMap

DiskDriveMap maps Win32_DiskDrive class to HardDisk class.

$Id: DiskDriveMap.py,v 1.4 2010/07/22 23:54:58 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]


from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.EnterpriseOIDs import EnterpriseOIDs

class DiskDriveMap(WMIPlugin):
    """Map Win32_DiskDrive class to HardDisk"""

    maptype = "HardDiskMap"
    modname = "ZenPacks.community.WMIPerf_Windows.Win32DiskDrive"
    relname = "harddisks"
    compname = "hw"

    tables = {
            "Win32_DiskDrive":
                (
                "Win32_DiskDrive",
                None,
                "root/cimv2",
                    {
                    '__path':'snmpindex',
                    'Caption':'description',
                    'Index':'id',
                    'InterfaceType':'diskType',
                    'Manufacturer':'_manuf',
                    'MediaType':'_mediatype',
                    'Model':'_model',
                    'SCSILogicalUnit':'bay',
                    'Size':'size',
                    },
                ),
            "Win32_PerfRawData_PerfDisk_PhysicalDisk":
                (
                "Win32_PerfRawData_PerfDisk_PhysicalDisk",
                None,
                "root/cimv2",
                    {
                    '__path':'snmpindex',
                    'Name':'name',
                    },
                ),
            }

    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        perfnames = {}
        instances = results.get("Win32_PerfRawData_PerfDisk_PhysicalDisk", None)
        if instances:
            for instance in instances:
                perfnames[instance['name'].split()[0]] = instance['snmpindex']
        instances = results.get("Win32_DiskDrive", None)
        if not instances: return
        for instance in instances:
            om = self.objectMap(instance)
            om.id = self.prepId('PHYSICALDRIVE%s'%om.id)
            try:
                if not om._mediatype or not om._mediatype.startswith('Fixed'):
                    continue
                om.perfindex = perfnames.get(str(instance['id']), None)
                if not om.perfindex: continue
                if om._model and not om._manuf: om._manuf = om._model.split()[0]
                if om._manuf not in EnterpriseOIDs.values(): om._manuf='Unknown'
                if om._model: om.setProductKey = MultiArgs(om._model, om._manuf)
            except AttributeError:
                raise
            rm.append(om)
        return rm
