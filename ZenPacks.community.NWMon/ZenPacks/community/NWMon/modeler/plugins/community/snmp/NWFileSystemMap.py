################################################################################
#
# This program is part of the NWMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""NWFileSystemMap

NWFileSystemMap maps the interface and ip tables to interface objects

$Id: NWFileSystemMap.py,v 1.0 2008/11/13 16:26:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class NWFileSystemMap(SnmpPlugin):

    maptype = "FileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "ZenPacks.community.NWMon.NWFileSystem"
    deviceProperties =  \
      SnmpPlugin.deviceProperties + ('zNWFileSystemMapIncludeNames',)


    snmpGetTableMaps = (
        GetTableMap('nwFSVolTable',
	            '.1.3.6.1.4.1.23.2.28.2.14.1',
                    {
                         '.1': 'snmpindex',
                         '.2': 'mount',
                         '.3': 'totalBlocks',
                         '.7': 'blockSize',
                         '.11': 'totalFiles',
	                 '.15': 'maxNameLen',
                         '.16': 'type',
                    }
	),
    )

    fsMaxNameLen = [ 0, 0, 0, 80, 256, 256] 

    def process(self, device, results, log):
        """collect snmp information from this device"""
	import re
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        fstable = tabledata.get("nwFSVolTable")
        skipfsnames = getattr(device, 'zNWFileSystemMapIncludeNames', None)
        rm = self.relMap()
        for fs in fstable.values():
            if not fs.has_key("totalBlocks"): continue
            if not (not skipfsnames or re.search(skipfsnames,fs['mount'])): continue
            om = self.objectMap(fs)
	    om.maxNameLen = self.fsMaxNameLen[om.maxNameLen]
            om.totalBlocks = om.totalBlocks * 1024 / om.blockSize
            om.id = self.prepId(om.mount)
            rm.append(om)
        return rm


