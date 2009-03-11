__doc__="""NetWareMemoryInfo

__version__ = '$Revision: 0.1'"""
import re

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
import Globals

class NetWareMemoryInfo(SnmpPlugin):

    maptype = "NetwareMemoryInfo"
    compname = "hw"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"

    snmpGetMap = GetMap({ 
        '.1.3.6.1.2.1.25.2.2.0': 'totalMemory',
        })

    def process(self, device, results, log):
         log.info('processing %s for device %s', self.name(), device.id)
         getdata, tabledata = results
         om = self.objectMap(getdata)
         om.totalMemory= om.totalMemory * 1024 
         return om

