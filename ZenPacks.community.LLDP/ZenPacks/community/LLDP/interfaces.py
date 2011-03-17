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

__doc__ = """interfaces.py
A Layer2 Link discovered by LLDP, for now a OS Component"""

__version__ = "0.1"

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class ILLDPLink(IComponentInfo):
    locPortDesc = schema.Text(title=u"Local Port", readonly=True)
    remSysName = schema.Text(title=u"Remote Sys", readonly=True)
    remPortDesc = schema.Text(title=u"Remote Port", readonly=True)
    remMgmtAddr = schema.Text(title=u"Remote Mgmt Ip", readonly=True)
    localInterface = schema.Entity(title=u"Local Interface", readonly=True)
    remoteDevice = schema.Entity(title=u"Remote System", readonly=True)
    remoteInterface = schema.Entity(title=u"Remote Interface", readonly=True)
