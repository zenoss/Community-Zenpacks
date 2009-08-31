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

class IBM3584DeviceMap(SnmpPlugin):
    """Map MIB elements from the 3584's SNMP to get serial number, model, etc
    """

    maptype = "IBM3584DeviceMap"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2.6.182.3.3.4.0': 'setOSProductKey',	# OS Version
        '.1.3.6.1.4.1.2.6.182.3.3.1.0' : 'setHWProductKey',	# HW Model
        '.1.3.6.1.4.1.2.6.182.3.3.2.0' : 'setHWSerialNumber',	# Serial 
         })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
        om = self.objectMap(getdata)
        return om

