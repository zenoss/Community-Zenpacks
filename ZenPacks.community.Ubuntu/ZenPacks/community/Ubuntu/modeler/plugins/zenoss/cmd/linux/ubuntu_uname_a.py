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
import re

class ubuntu_uname_a(CommandPlugin):

    maptype = "DeviceMap"
    compname = ""
    command = 'uname -a && echo __COMMAND__ && cat /etc/lsb-release'
    descPattern = re.compile(r"DISTRIB_DESCRIPTION=\"(.*)\"")
    codenamePattern = re.compile(r"DISTRIB_CODENAME=(.*)")

    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing the uname -a info for device %s" % device.id)
        uname, ubuntutype = results.split('__COMMAND__\n')
        ubuntutype=ubuntutype.strip('\n')
        for line in ubuntutype.split('\n'):
            p = self.descPattern.search(line)
            if p:
                desc=p.group(1)
            p = self.codenamePattern.search(line)
            if p:
                codename=p.group(1)
        ubuntutype="%s (%s)" % (desc,codename)
        om = self.objectMap()
        om.snmpDescr = uname.strip()
        om.setHWProductKey, om.snmpSysName, kernelRelease = uname.split()[:3]
        om.setOSProductKey = " ".join([om.setHWProductKey, kernelRelease])
        om.setOSProductKey = MultiArgs(om.setOSProductKey,ubuntutype)
        log.debug("snmpSysName=%s, setOSProductKey=%s" % (
                om.snmpSysName, om.setOSProductKey))
        return om

