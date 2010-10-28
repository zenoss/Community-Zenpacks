###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, 2009 Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__ = """UCDFileSystemMap

UCDFileSystemMap maps the filesystems to filesystem objects

"""

import re

from Products.ZenUtils.Utils import unsigned
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetTableMap

class UCDFileSystemMap(SnmpPlugin):

    maptype = "FileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    deviceProperties = SnmpPlugin.deviceProperties + (
      'zFileSystemMapIgnoreNames',)

    columns = {
         '.1': 'snmpindex',
         '.2': 'mount',
         '.3': 'storageDevice',
         '.6': 'totalBlocks',
         }

    snmpGetTableMaps = (
        GetTableMap('fsTableOid', '.1.3.6.1.4.1.2021.9.1', columns),
    )

    def process(self, device, results, log):
        """Process SNMP information from this device"""
        log.info('Modeler %s processing data for device %s', self.name(), device.id)
        getdata, tabledata = results
        log.debug("%s tabledata = %s", device.id, tabledata)
        fstable = tabledata.get("fsTableOid")
        if fstable is None:
            log.error("Unable to get data for %s from fsTableOid"
                          " -- skipping model" % device.id)
            return None

        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        maps = []
        rm = self.relMap()
        for fs in fstable.values():
            if not self.checkColumns(fs, self.columns, log):
                continue
            
            totalBlocks = fs['totalBlocks']

            # This may now be a redundant check. Candidate for removal.
            #   http://dev.zenoss.org/trac/ticket/4556
            if totalBlocks < 0:
                fs['totalBlocks'] = unsigned(totalBlocks)

            # blockSize is not used by UCD mibs.
            # UCD mibs display size in kilobytes.
            # Value has been hardcoded as 1024 to convert to bytes.
            fs['blockSize'] = 1024
            size = fs['totalBlocks']

            # UCD-SNMP-MIB does not provide filesystem type info.
            # Only zFileSystemMapIgnoreNames is checked.
            if skipfsnames and re.search(skipfsnames, fs['mount']):
                log.info("Skipping %s as it matches zFileSystemMapIgnoreNames.",
                    fs['mount'])
                continue
            
            om = self.objectMap(fs)
            om.id = self.prepId(om.mount)
            rm.append(om)
        maps.append(rm)
        return maps
