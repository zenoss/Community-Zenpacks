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

from zope.interface import implements
from Products.Zuul.decorators import info
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from ZenPacks.community.LLDP import interfaces

from Products.Zuul.interfaces import IInfo

import logging
log = logging.getLogger('LLDP')


class LLDPLinkInfo(ComponentInfo):
    implements(interfaces.ILLDPLink)

    locPortDesc = ProxyProperty("locPortDesc")
    remSysName = ProxyProperty("remSysName")
    remPortDesc = ProxyProperty("remPortDesc")
    remMgmtAddr = ProxyProperty("remMgmtAddr")

    @property
    @info
    def localInterface(self):
        interface = self._object.localInterface()
        try:
            log.warn("localInterface Info for %s the name is %s" % \
                (interface, interface.name))
        except:
            log.warn("localInterface Info can't log")
        return interface

    @property
    @info
    def remoteInterface(self):
        return self._object.remoteInterface()

    @property
    @info
    def remoteDevice(self):
        return self._object.remoteDevice()

    monitor = False  # not polled, only during model, no graphs
