#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap

class AlvarionWI2DeviceMap(SnmpPlugin):
    """Map mib elements from Alvarion mib to get hw and os products.
    """

    maptype = "AlvarionWI2DeviceMap" 

    snmpGetMap = GetMap({ 
     
       '.1.3.6.1.4.1.12394.1.10.5.4.2.1.1.8.6' : 'manufacturer',
       '.1.3.6.1.4.1.12394.1.10.5.4.2.1.1.9.6' : 'setHWProductKey',
       '.1.3.6.1.4.1.12394.1.10.5.6.1.1.5.0' : 'setHWSerialNumber',       
       '.1.3.6.1.4.1.12394.1.10.5.6.1.1.2.0': 'setOSProductKey',
         })

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
        om = self.objectMap(getdata)
        return om




