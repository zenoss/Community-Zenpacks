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

import Globals
import os.path
from Products.ZenModel.ZenPack import ZenPackBase


# inject relation into OperatingSystem
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenRelations.RelSchema import *
OperatingSystem._relations += ((
    "lldplinks",
    ToManyCont(ToOne, "ZenPacks.community.LLDP.LLDPLink", "os")),)

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())


class ZenPack(ZenPackBase):
    """ ZenPack loader
    """
    def install(self, app):
        ZenPackBase.install(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

    def remove(self, app, junk):
        ZenPackBase.remove(self, app, junk)
        OperatingSystem._relations = tuple(
            [x for x in OperatingSystem._relations
            if x[0] not in ['lldplinks', ]])
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()
