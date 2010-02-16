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

$Id: DeviceMap.py,v 1.0 2010/02/16 16:29:54 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.EnterpriseOIDs import EnterpriseOIDs

class DiskDriveMap(WMIPlugin):
    """Map Win32_DiskDrive class to HardDisk"""

    maptype = "HardDiskMap"
    modname = "Products.ZenModel.HardDisk"
    relname = "harddisks"
    compname = "hw"

    def queries(self):
        return {
            "Win32_DiskDrive":
                (
                "Win32_DiskDrive",
                None,
                "root/cimv2",
                    {
		    'Caption':'description',
		    'Index':'id',
                    'Manufacturer':'_manuf',
		    'MediaType':'_mediatype',
                    'Model':'_model',
                    },
                ),
            "Win32_PerfRawData_PerfDisk_PhysicalDisk":
                (
                "Win32_PerfRawData_PerfDisk_PhysicalDisk",
                None,
                "root/cimv2",
                    {
                    'Name':'_name',
                    },
                ),
            }

    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
	perfnames = {}
	instances = results["Win32_PerfRawData_PerfDisk_PhysicalDisk"]
	if instances:
	    for instance in instances:
	        perfnames[instance['_name'].split()[0]] = instance['_name']
	instances = results["Win32_DiskDrive"]
	if not instances: return
	for instance in instances:
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
	    try:
	        if not om._mediatype or not om._mediatype.startswith('Fixed'):
		    continue
                om.snmpindex = perfnames.get(om.id, None)
	        if not om.snmpindex: continue
	        if om._manuf not in EnterpriseOIDs.values():
	            om._manuf = 'Unknown'
	        if om._model:
	            om.setProductKey = MultiArgs(om._model, om._manuf)
            except AttributeError:
                continue
            rm.append(om)
        return rm
