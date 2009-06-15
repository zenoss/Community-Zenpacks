
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap

class AIXDeviceMap(SnmpPlugin):
    """Map AIX MIB to get hw and os products.
    """

    maptype = "AIXDeviceMap" 

    snmpGetMap = GetMap({ 
        '.1.3.6.1.4.1.2.6.191.1.3.6' : 'setHWProductKey',
        '.1.3.6.1.4.1.2.6.191.1.3.7' : 'setHWSerialNumber',
         })


    def process(self, device, results, log):
        """collect snmp information from this device"""

        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        if getdata['setHWProductKey'] is None:
           return None

        om = self.objectMap(getdata)

        om.setHWProductKey=MultiArgs(om.setHWProductKey,"IBM")
        #
        # There's existing logic in the NewDeviceMap.py plugin to find
        # the OS version etc, so we won't set the setOsProductKey field.
        #
        return om
