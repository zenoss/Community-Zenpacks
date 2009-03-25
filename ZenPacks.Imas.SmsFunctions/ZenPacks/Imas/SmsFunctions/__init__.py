###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2008, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ SMS loader
    """

    packZProperties = [
            ('zSmsBetween0', '06:00 till 22:00', 'string'),
	    ('zSmsBetween1', '06:00 till 22:00', 'string'),
	    ('zSmsNumber0', 'support', 'string'),
            ('zSmsNumber1', 'support', 'string'),
	    ('zSmsSend0', 'False', 'boolean'),
	    ('zSmsSend1', 'False', 'boolean'),
            ]



