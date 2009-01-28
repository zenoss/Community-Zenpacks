###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
# Created By  :  Wouter D'Haeseleer
# Created On  :  05-11-2007
# Company     :  Imas NV
#
###########################################################################

import re

from CollectorPlugin import CommandPlugin

class VmwareEsxDf(CommandPlugin):
    """
    Run vdf to model filesystem information. Should work on all ESX servers.
    """
    maptype = "FilesystemMap"
    command = '/usr/sbin/vdf'
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"

    def process(self, device, results, log):
        log.info('Collecting filesystems for device %s' % device.id)
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        rm = self.relMap()
        rlines = results.split("\n")
        bline = ""
        for line in rlines:
            if line.startswith("Filesystem"): continue
            om = self.objectMap()
            spline = line.split()
            if len(spline) == 1:
                bline = spline[0]
                continue
            if bline:
                spline.insert(0,bline)
                bline = None
            if len(spline) != 6: continue
            (om.storageDevice, tblocks, u, a, p, om.mount) = spline
            if skipfsnames and re.search(skipfsnames,om.mount): continue
            om.totalBlocks = long(tblocks)
            om.blockSize = 1024
            om.id = self.prepId(om.mount)
            rm.append(om)
        return rm
