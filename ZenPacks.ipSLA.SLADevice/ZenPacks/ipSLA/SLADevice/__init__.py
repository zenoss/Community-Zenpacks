__doc__="ipSLA ZenPack"

import Globals
import os
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.ZenPack import ZenPackBase

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())


import ZenPacks.ipSLA.SLADevice
def initialize(registrar):
	registrar.registerClass(
		SLAS.SLAS,
		permission='Add DMD Objects',
	)