###########################################################################
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

class MrvDeviceMap(SnmpPlugin):
    """Map mib elements from Mrv mib to get hw and os products.
    """

    maptype = "MrvDeviceMap" 

    snmpGetMap = GetMap({ 
        '.1.2.840.10036.3.1.2.1.2.2' : 'manufacturer',
        '.1.2.840.10036.3.1.2.1.3.2' : 'setHWProductKey',
        '.1.3.6.1.2.1.2.2.1.6.1' : 'setHWSerialNumber',
        '.1.3.6.1.4.1.629.6.16.2.1.3': 'setOSProductKey',
         })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
        om = self.objectMap(getdata)
        return om



