__doc__="""FileSystemMap

FileSystemMap maps the interface and ip tables to interface objects

$Id: HRFileSystemMap.py,v 1.2 2004/04/07 16:26:53 edahl Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

import re

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
import Globals

class HPUXFileSystemMap(SnmpPlugin):

    maptype = "FileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "ZenPacks.community.HPUXMonitor.HPUXFileSystem"

    columns = {
         '.1': 'snmpindex',
         '.2': 'type',
         '.4': 'totalBlocks',
         '.7': 'blockSize',
         '.10': 'mount',
         }

    ocolumns = {
         '.1': 'snmpindex',
         '.2': 'type',
         '.3': 'storageDevice',
         '.4': 'totalBlocks',
         '.5': 'blocksFree',
         '.6': 'blocksAvail',
         '.7': 'blockSize',
         '.8': 'totalFiles',
         '.9': 'filesFree',
         '.10': 'mount',
         }

    fstypemap = {
        0: 'hfs',
        7: 'vxfs',
        }

    snmpGetTableMaps = (
        GetTableMap('fsTableOid', '.1.3.6.1.4.1.11.2.3.1.2.2.1', columns),
    )



    def process(self, device, results, log):
        """collect snmp information from this device"""
        getdata, tabledata = results
        fstable = tabledata.get("fsTableOid")
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        maps = []
        rm = self.relMap()
        for fs in fstable.values():
            if not fs.has_key("totalBlocks"): continue
            if not self.checkColumns(fs, self.columns, log): continue
            fs['snmpindex'] = '%s.%s' % (fs['snmpindex'],fs['type'])
            fs['type'] = self.fstypemap.get(fs['type'],None)
            size = long(fs['blockSize'] * fs['totalBlocks'])
            if size > 0:
                om = self.objectMap(fs)
                om.id = self.prepId(om.mount)
                rm.append(om)
        maps.append(rm)
        return maps

