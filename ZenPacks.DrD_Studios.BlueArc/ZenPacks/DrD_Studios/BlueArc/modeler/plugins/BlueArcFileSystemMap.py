
import Globals
import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class BlueArcFileSystemMap(SnmpPlugin):

    maptype = "BlueArcFileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    volumeCapacity = ''
    volumeFreeCapacity = ''

    if hasattr(SnmpPlugin, "deviceProperties"):
        deviceProperties = SnmpPlugin.deviceProperties + \
                           ('zFileSystemMapIgnoreNames',)



    columns = {
        '.1': 'volumeSysDriveIndex',
        '.2': 'volumePartitionID',
        '.3': 'volumeLabel',
        '.4': 'volumeStatus',
        '.5': 'volumeCapacity',
        '.6': 'volumeFreeCapacity',
        '.7': 'volumeEnterpriseVirtualServer',
        }

    snmpGetTableMaps = (
        GetTableMap('volumeTable', '.1.3.6.1.4.1.11096.6.1.1.1.3.5.2.1', columns),
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

        rm = self.relMap()
        for fs in results[1].get('volumeTable').values():
            # Sanity checks
            if not self.checkColumns(fs, self.columns, log): continue

            volumeCapacity = fs['volumeCapacity']
         
            # Create the object map which puts our SNMP stats into
            # the FileSystem object
            om             = self.objectMap()
            om.id          = self.prepId(fs['volumeLabel'])
            om.snmpindex   = str(fs['volumeSysDriveIndex'])
            om.mount       = fs['volumeLabel']
            om.type        = self.__class__.typemap['fixedDisk']
            om.blockSize   = 1024
            om.totalBlocks = volumeCapacity/1024
            rm.append(om)

        return [rm, ]


