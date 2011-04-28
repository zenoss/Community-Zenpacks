################################################################################
# 
# This file is part of ZenPacks.community.LLDP
#
# Copyright (C) 2011 GSI Helmholtzzentrum fuer Schwerionenforschung Gmbh
#                    Christoph Handel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
################################################################################

__doc__ = """A Layer2 Link discovered by LLDP, for now a OS Component"""

__version__ = "0.1"

# from Globals import DTMLFile
# from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

# from Products.ZenModel.DeviceComponent import DeviceComponent
# from Products.ZenModel.ManagedEntity import ManagedEntity

from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.OSComponent import OSComponent
from Products.ZenUtils.Utils import prepId

import logging
log = logging.getLogger('LLDP')


class LLDPLink(OSComponent):
    """LLDP Link information"""

    portal_type = meta_type = 'LLDPLink'

    _properties = OSComponent._properties + (
        {'id': 'locPortDesc', 'type': 'string', 'mode': ''},
        {'id': 'locIndex',    'type': 'string', 'mode': ''},
        {'id': 'remPortDesc', 'type': 'string', 'mode': ''},
        {'id': 'remSysName',  'type': 'string', 'mode': ''},
        {'id': 'remMgmtAddr', 'type': 'string', 'mode': ''},
        )

    _relations = OSComponent._relations + ((
        "os",
        ToOne(ToManyCont,
            "Products.ZenModel.OperatingSystem",
            "lldplinks")
        ),)

    locPortDesc = "unknown"
    locIndex = ""
    remPortDesc = "unknown"
    remSysName = "unknown"
    remMgmtAddr = "unknown"
    remlink = "unknown"

    def _remoteIp(self):
        """get IpInterface Object for remote address"""
        if not self.remMgmtAddr:
            return None
        log.warn("searching for ip %s" % self.remMgmtAddr)
        ip = self.dmd.Networks.findIp(self.remMgmtAddr)
        log.warn("found %s" % ip)
        return ip

    def _interfaceByDesc(self, device, desc):
        try:
            interface = device.os.interfaces._getOb(prepId(desc))
        except:
            # catch all, bad, but lazy
            log.warn("can't find interface %s on device %s" % (desc, device))
            return desc
        return interface

    def localInterface(self):
        log.warn("localInterface called")
        return self._interfaceByDesc(self.device(), self.locPortDesc)

    def remoteDevice(self):
        """try to get the remote device, using the management IP"""
        ip = self._remoteIp()
        if ip:
            if ip.device() is None:
                return self.remSysName
            else:
                return ip.device()
        else:
            return self.remSysName

    def remoteInterface(self):
        ip = self._remoteIp()
        if not ip:
            return self.remPortDesc
        device = ip.device()
        if not device:
            return self.remPortDesc
        return self._interfaceByDesc(device, self.remPortDesc)

InitializeClass(LLDPLink)
