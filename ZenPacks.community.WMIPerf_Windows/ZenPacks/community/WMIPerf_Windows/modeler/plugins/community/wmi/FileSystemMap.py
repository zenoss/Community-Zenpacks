################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""FileSystemMap

FileSystemMap maps the CIM_FileSystem class to filesystems objects

$Id: FileSystemMap.py,v 1.2 2010/07/23 00:00:01 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

import re
from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId

class FileSystemMap(WMIPlugin):

    maptype = "FileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    deviceProperties = WMIPlugin.deviceProperties + (
      'zFileSystemMapIgnoreNames', 'zFileSystemMapIgnoreTypes')

    tables = {
            "Win32_LogicalDisk":
                (
                "Win32_LogicalDisk",
                None,
                "root/cimv2",
                    {
                    'MaximumComponentLenght':'maxNameLen',
                    'Size':'totalBlocks',
                    'BlockSize':'blockSize',
                    'Name':'mount',
                    'FileSystem':'type',
                    }
                ),
            }

    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results.get("Win32_LogicalDisk", None)
        if not instances: return
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        skipfstypes = getattr(device, 'zFileSystemMapIgnoreTypes', None)
        for instance in instances:
            try:
                if skipfsnames and re.search(skipfsnames, instance['mount']):
                    log.info("Skipping %s as it matches zFileSystemMapIgnoreNames.",
                        instance['mount'])
                    continue
                if skipfstypes and instance['type'] in skipfstypes:
                    log.info("Skipping %s (%s) as it matches zFileSystemMapIgnoreTypes.",
                        instance['mount'], instance['type'])
                    continue
                om = self.objectMap(instance)
                om.id = prepId(om.mount)
                om.snmpindex = om.id
                if getattr(om, 'blockSize', None) or om.blockSize == 0:
                    om.blockSize = 512
                if not om.totalBlocks: continue
                om.totalBlocks = om.totalBlocks / om.blockSize
            except AttributeError:
                continue
            rm.append(om)
        return rm
