__doc__="""NetWareFileSystemMap

FileSystemMap maps the interface and ip tables to interface objects

$Id: NetWareFileSystemMap.py,v 0.9 2009/03/09 efeldman"""

__version__ = '$Revision: 0.9 $'[11:-2]

import re

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
import Globals

class NetWareFileSystemMap(SnmpPlugin):

    maptype = "FileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    deviceProperties =  \
      SnmpPlugin.deviceProperties + ('zFileSystemMapIgnoreNames',)


    columns = {
        '.1': 'nwVolId',
        '.2': 'nwVolPhysicalName',
        '.3': 'nwVolSize',
        '.4': 'nwVolFree',
        '.5': 'nwVolFreeable',
        '.6': 'nwVolNonFreeable',
        '.7': 'nwVolBlockSize',
        '.8': 'nwVolMounted',
        '.15': 'nwVolFileSystemID',
        }

    snmpGetTableMaps = (
        GetTableMap('nwFSTable', '.1.3.6.1.4.1.23.2.28.2.14.1', columns),
    )

    nwVolFileSystemID = {
        3: 'netware',
        5: 'nss',
        }


    def process(self, device, results, log):
        """collect snmp information from this device"""
        getdata, tabledata = results
        fstable = tabledata.get( "nwFSTable" )
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        maps = []
        rm = self.relMap()
        for fs in fstable.values():
            if not fs.has_key("nwVolSize"): continue
            if not self.checkColumns(fs, self.columns, log): continue
            if fs['nwVolSize'] > 0 and (not skipfsnames or not re.search(skipfsnames,fs['nwVolPhysicalName'])):
                om             = self.objectMap()
                om.id          = self.prepId(fs['nwVolPhysicalName'])
                om.snmpindex   = fs['nwVolId']
                om.mount       = fs['nwVolPhysicalName']
                om.type        = fs['nwVolFileSystemID']
                om.blockSize   = 1024
                om.totalBlocks = fs['nwVolSize']
                rm.append(om)
        maps.append(rm)
        return maps


