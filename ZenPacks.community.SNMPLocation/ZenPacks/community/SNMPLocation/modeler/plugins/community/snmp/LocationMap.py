from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap

class LocationMap(SnmpPlugin):
    
    maptype = "LocationMap"

    snmpGetMap = GetMap({
            '.1.3.6.1.2.1.1.6.0' : 'setLocationviaSNMP',
            })
    
    def process(self, device, results, log):
        """Collect SNMP location information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        om = self.objectMap(getdata)
        om.setLocationviaSNMP = '/%s' % (self.prepId(om.setLocationviaSNMP))
        
        log.info('Location: %s', om.setLocationviaSNMP)
        return om

