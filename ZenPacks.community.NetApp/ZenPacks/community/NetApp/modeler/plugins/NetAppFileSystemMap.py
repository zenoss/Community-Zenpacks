
import Globals
import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class NetAppFileSystemMap(SnmpPlugin):

    maptype = "NetAppFileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    dfKBytesTotal = ''
    dfLowTotalKBytes = ''
    dfHighTotalKBytes = ''

    if hasattr(SnmpPlugin, "deviceProperties"):
        deviceProperties = SnmpPlugin.deviceProperties + \
                           ('zFileSystemMapIgnoreNames',)

    columns = {
        '.1': 'dfIndex',
        '.2': 'dfFileSys',
        '.3': 'dfKBytesTotal',
        '.7': 'dfInodesUsed',
        '.8': 'dfInodesFree',
        '.9': 'dfPerCentInodeCapacity',
	'.11': 'dfMaxFilesAvail',
        '.14': 'dfHighTotalKBytes',
        '.15': 'dfLowTotalKBytes',

        }

    snmpGetTableMaps = (
        GetTableMap('dfTable', '.1.3.6.1.4.1.789.1.5.4.1', columns),
    )

    typemap = {
        "fixedDisk": ".1.3.6.1.2.1.25.2.1.4",
        }


    def process(self, device, results, log):
        """collect snmp information from this device"""

        # log that we're here
        log.info('processing %s for device %s', self.name(), device.id)

        # Get the skipped fs name regex
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)

        # Iterate over the rows in the table
        rm = self.relMap()
        for fs in results[1].get('dfTable').values():
            # Sanity checks
            if not self.checkColumns(fs, self.columns, log): continue
            if not fs['dfFileSys'].endswith("/"): continue
            fs['dfFileSys'] = fs['dfFileSys'].split("/")[-2]
            if skipfsnames and re.search(skipfsnames, fs['dfFileSys']): continue

            dfLowTotalKBytes = fs['dfLowTotalKBytes']
         
            if fs['dfLowTotalKBytes'] < 0:
                dfHighTotalKBytes = (fs['dfHighTotalKBytes'] + 1) *  2 ** 32 
            else:
                dfHighTotalKBytes = fs['dfHighTotalKBytes'] * 2 ** 32

            # Create the object map which puts our SNMP stats into
            # the FileSystem object
            om             = self.objectMap()
            om.id          = self.prepId(fs['dfFileSys'])
            om.snmpindex   = fs['dfIndex']
            om.mount       = fs['dfFileSys']
            om.type        = self.__class__.typemap['fixedDisk']
            om.blockSize   = 1024
            om.totalBlocks = dfHighTotalKBytes + dfLowTotalKBytes
	    om.totalFiles  = fs['dfMaxFilesAvail'] # confusing eh? ......
            rm.append(om)

        return [rm, ]


