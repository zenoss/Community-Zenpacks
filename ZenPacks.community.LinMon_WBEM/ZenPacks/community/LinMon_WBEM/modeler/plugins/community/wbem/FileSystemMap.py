################################################################################
#
# This program is part of the LinMon_WBEM Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""FileSystemMap

FileSystemMap maps the CIM_FileSystem class to filesystems objects

$Id: FileSystemMap.py,v 1.0 2010/02/21 20:52:10 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

import re
from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.ZenUtils.Utils import prepId

class FileSystemMap(WBEMPlugin):

    maptype = "FileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    deviceProperties = WBEMPlugin.deviceProperties + (
      'zFileSystemMapIgnoreNames', 'zFileSystemMapIgnoreTypes')

    tables = {
            "CIM_FileSystem":
                (
                "CIM_FileSystem",
                None,
                "root/cimv2",
                    {
                    '__path':'snmpindex',
                    'MaxFileNameLength':'maxNameLen',
                    'BlockSize':'blockSize',
                    'FileSystemSize':'totalBlocks',
                    'Root':'mount',
                    'FileSystemType':'type',
                    }
                ),
            }

    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results["CIM_FileSystem"]
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
                if not om.totalBlocks or not om.blockSize: continue
                om.totalBlocks = om.totalBlocks / om.blockSize
            except AttributeError:
                continue
            rm.append(om)
        return rm
