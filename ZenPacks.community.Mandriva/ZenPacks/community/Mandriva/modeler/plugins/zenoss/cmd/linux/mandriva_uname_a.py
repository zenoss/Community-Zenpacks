# -*- coding: utf-8 -*-
###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

_doc__ = """uname -a
Determine snmpSysName and setOSProductKey from the result of the uname -a
command.
"""

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class mandriva_uname_a(CommandPlugin):

    maptype = "DeviceMap"
    compname = ""
    command = 'uname -a && echo __COMMAND__ && cat /etc/mandrakelinux-release | head -1'

    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing the uname -a info for device %s" % device.id)
        uname, mandrivatype = results.split('__COMMAND__\n')
        mandrivatype=mandrivatype.strip('\n')
        om = self.objectMap()
        om.snmpDescr = uname.strip()
        om.setHWProductKey, om.snmpSysName, kernelRelease = uname.split()[:3]
        om.setOSProductKey = " ".join([om.setHWProductKey, kernelRelease])
        om.setOSProductKey = MultiArgs(om.setOSProductKey,mandrivatype)
        log.debug("snmpSysName=%s, setOSProductKey=%s" % (
                om.snmpSysName, om.setOSProductKey))
        return om
