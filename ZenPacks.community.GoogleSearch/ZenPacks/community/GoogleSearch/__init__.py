###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import logging
log = logging.getLogger('zen.GoogleSearch')

import os
import Globals
from Products.CMFCore.DirectoryView import registerDirectory


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPack as ZenPackBase

class ZenPack(ZenPackBase):
    """
    Customize ZenPack class to allow additional installation and removal steps.
    """
    
    def install(self, dmd):
        super(ZenPack, self).install(dmd)
        
    def remove(self, dmd, leaveObjects=False):
        super(ZenPack, self).remove(dmd, leaveObjects)

