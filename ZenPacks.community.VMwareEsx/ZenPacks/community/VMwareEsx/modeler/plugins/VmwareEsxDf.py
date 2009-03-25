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

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

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

#[root@esx1 root]# vdf -P
#Filesystem         1024-blocks      Used Available Capacity Mounted on
#/dev/sda2              5036316   3384756   1395728      71% /
#/dev/sda1               101089     26275     69595      28% /boot
#none                    134284         0    134284       0% /dev/shm
#/dev/sda6              2008108    153748   1752352       9% /var/log
#/vmfs/devices       8458327184         08458327184   0% /vmfs/devices
#/vmfs/volumes/476c3cd3-328506b3-5297-001e4f11aa50      576716800 435473408 141243392  75% /vmfs/volumes/esx1store
#/vmfs/volumes/48906e44-348d58e0-3279-0015177d607c     19815464961753621504 227924992  88% /vmfs/volumes/FAS2020-DEV
#/vmfs/volumes/48906e9d-71729353-bfb1-0015177d607c      232783872 159772672  73011200  68% /vmfs/volumes/FAS2020-AUX

