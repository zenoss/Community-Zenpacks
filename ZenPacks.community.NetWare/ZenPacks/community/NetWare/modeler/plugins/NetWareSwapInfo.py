__doc__="""NetWareSwapInfo

__version__ = '$Revision: 0.1'"""
import re

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
import Globals

class NetWareSwapInfo(SnmpPlugin):

    maptype = "NetwareSwapInfo"
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"

    snmpGetMap = GetMap({ 
        '.1.3.6.1.4.1.23.2.79.7.1.5.0': 'totalSwap',
        })

    def process(self, device, results, log):
         log.info('processing %s for device %s', self.name(), device.id)
         getdata, tabledata = results
         om = self.objectMap(getdata)
         om.totalSwap= om.totalSwap * 4
         return om
