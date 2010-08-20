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

class RaytalkCPEDeviceMap(SnmpPlugin):
    """Map mib elements from Raytalk mib to get hw and os products.
    """

    maptype = "RaytalkCPEDeviceMap" 

    snmpGetMap = GetMap({ 
       # 'Raytalk' : 'manufacturer',
       # 'cpe2.4' : 'setHWProductKey',
       # '.1.2.840.10036.1.1.1.1.0' : 'setHWSerialNumber',
       # '.1.2.840.10036.3.1.2.1.4.0': 'setOSProductKey',
         })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
        om = self.objectMap(getdata)
        return om


