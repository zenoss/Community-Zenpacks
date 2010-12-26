################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""VolumeFileSystemMap

VolumeFileSystemMap maps the Win32_Volume class to filesystems objects

$Id: VolumeFileSystemMap.py,v 1.0 2010/12/21 18:47:59 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

import re
from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin

class VolumeFileSystemMap(WMIPlugin):

    maptype = "VolumeFileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    deviceProperties = WMIPlugin.deviceProperties + (
      'zFileSystemMapIgnoreNames', 'zFileSystemMapIgnoreTypes')

    tables = {
            "Win32_Volume":
                (
                "Win32_Volume",
                None,
                "root/cimv2",
                    {
                    '__path':'snmpindex',
                    'BlockSize':'blockSize',
                    'Capacity':'totalBlocks',
                    'FileSystem':'type',
                    'MaximumFileNameLength':'maxNameLen',
                    'Name':'mount',
                    }
                ),
            }

    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        skipfstypes = getattr(device, 'zFileSystemMapIgnoreTypes', None)
        for instance in results.get("Win32_Volume", []):
            try:
                if skipfsnames and re.search(skipfsnames, instance['mount']):
                    log.info("Skipping %s as it matches zFileSystemMapIgnoreNames.",
                        instance['mount'])
                    continue
                if skipfstypes and instance['type'] in skipfstypes:
                    log.info("Skipping %s (%s) as it matches zFileSystemMapIgnoreTypes.",
                        instance['mount'], instance['type'])
                    continue
                if "\Volume{" in instance['mount']: continue
                instance['mount'] = instance['mount'][:-1]
                om = self.objectMap(instance)
                om.id = self.prepId(om.mount)
                if ':' in om.snmpindex:om.snmpindex=om.snmpindex.split(':',1)[1]
                om.blockSize = getattr(om, 'blockSize', 512) or 512
                if not om.totalBlocks: continue
                om.totalBlocks = om.totalBlocks / om.blockSize
            except AttributeError:
                continue
            rm.append(om)
        return rm
