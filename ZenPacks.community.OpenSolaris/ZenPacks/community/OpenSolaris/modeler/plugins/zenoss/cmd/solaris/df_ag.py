###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__ = """df -ag
Determine the filesystems to monitor
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class df_ag(CommandPlugin):
    """
    Run df -ag to model filesystem information.
    """
    maptype = "FilesystemMap" 
    command = '/bin/df -ag'
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    deviceProperties = \
                CommandPlugin.deviceProperties + ('zFileSystemMapIgnoreNames',)

    oses = ['SunOS']
    #mount = ""
    #storageDevice = ""
    #type = ""
    #blockSize = 0
    #totalBlocks = 0L
    #totalFiles = 0L
    #capacity = 0
    #inodeCapacity = 0
    #maxNameLen = 0

    scanners = [
            '(?P<availBlocks>\d+) free blocks',
            '(?P<totalBlocks>\d+) total blocks',
            '(?P<availInodes>\d+) free files',
            '(?P<totalInodes>\d+) total files',
            '(?P<blockSize>\d+) block size',
            '(?P<fstype>\w+) fstype',
            ]

    def condition(self, device, log):
        return device.os.uname == '' or device.os.uname in self.oses


    def process(self, device, results, log):
        log.info('Collecting filesystems for device %s' % device.id)
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        skipfstypes = getattr(device, 'zFileSystemMapIgnoreTypes', None)
        rm = self.relMap()

        # split data into component blocks
        parts = results.split('\n\n')

        for part in parts:
            #print part
            # find the component match
            match = re.search('^(?P<component>[\w\/-]+)\s*', part)
            if not match: continue
            component = match.groupdict()['component'].strip()
            #print component

            om = self.objectMap()
            om.id = self.prepId(component)
            om.mount = component
            if skipfsnames and re.search(skipfsnames,om.mount): continue
            om.blockSize=None
            # find any data
            for search in self.scanners:
                #print search
                match = re.search(search, part)
                if match:
                    for name, value in match.groupdict().items():
                        #print name
                        #print value
                        if name == 'availBlocks': availBlocks = long(value)/2
                        if name == 'totalBlocks':
                            om.totalBlocks = long(value)/2
                            if om.totalBlocks == "-": om.totalBlocks = 0
                        if name == 'availInodes': availInodes = long(value)
                        if name == 'totalInodes': totalInodes = long(value)
                        if name == 'blockSize': om.blockSize = long(value)
                        if name == 'fstype':
                            om.type = str(value)
                            if skipfstypes and re.search(skipfstypes,om.type):continue

            # skip filesystems without a defined blocksize
            # eg proc filesystems etc ..
            if not om.blockSize: continue
            om.blockSize = 1024
            rm.append(om)
        #print rm
        return rm
