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
#
# Re-Edited By:	Randy Schneiderman
# Re-Edited On: 07/21/2008
# Comapany:	Stroz Friedberg
#
# New Comments: Based on the VMwareESX ZenPack, this plugin uses the same code
#		with the exception of the class name and the command use.
#		This has been successfully tested with EMC's Celerra Network 
#		Server v5.5.
#
###########################################################################

import re

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class CelerraDf(CommandPlugin):
    """
    Run server_df to model filesystem information. 
    """
    maptype = "FilesystemMap" 
    command = 'export NAS_DB=/nas && /nas/bin/server_df server_2'
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
