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
###########################################################################

__doc__ = """memory
Maps oracle tablespace layout 
"""

import sys

sys.path.append('/usr/local/zenoss/zenoss')

from Products.DataCollector.plugins.CollectorPlugin import LinuxCommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

#MULTIPLIER = {
#    'kB' : 1024,
#    'MB' : 1024 * 1024,
#    'b' : 1
#}


class memory(LinuxCommandPlugin):
    maptype = "FileSystemMap" 
    command = 'cat /tmp/oracle_ts'
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"


    def process(self, device, results, log):
        log.info('Collecting oracle tablespace for device %s' % device.id)

        rm = self.relMap()
        maps = []

        for line in results.split("\n"):
            vals = line.split(':')
            if len(vals) != 2:
                continue

            name, value = vals
            vals = value.split()
            if len(vals) != 2:
                continue
            
            value, unit = vals
            size = int(value) 
                
#            if name == 'MemTotal':
#                maps.append(ObjectMap({"totalMemory": size}, compname="hw"))
#            if name == 'SwapTotal':
#                maps.append(ObjectMap({"totalSwap": size}, compname="os"))
	    maps.append(ObjectMap({"totalMemory": size}, compname="hw"))
        return maps
