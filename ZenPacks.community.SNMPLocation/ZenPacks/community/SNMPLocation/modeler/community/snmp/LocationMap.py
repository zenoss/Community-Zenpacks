import re
import sys
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class LocationMap(SnmpPlugin):

    maptype = "LocationMap"

    snmpGetMap = GetMap({
             '.1.3.6.1.2.1.1.6.0' : 'setLocation',
             })

    def process(self, device, results, log):
        """Collect SNMP location information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        om = self.objectMap(getdata)
        om.setLocation = '/%s' % (self.prepId(om.setLocation))

        log.info('Location: %s', om.setLocation)
        return om

