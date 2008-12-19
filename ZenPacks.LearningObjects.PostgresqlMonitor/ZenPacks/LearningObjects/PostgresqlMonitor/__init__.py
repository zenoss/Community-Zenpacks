###########################################################################
#
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
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
    """ Postgresql loader
    """

    packZProperties = [
            ('zPostgresqlUsername', 'zenoss', 'string'),
            ('zPostgresqlPassword', 'password', 'string'),
	     ]
