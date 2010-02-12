
__doc__="HP Blade Chassis Zen Pack"

import Globals
import os

from Products.CMFCore.DirectoryView import registerDirectory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

import ZenPacks.community.HPBladeChassis
def initialize(registrar):
    registrar.registerClass(
    BladeServer.BladeServer,
    permission='Add DMD Objects',
    )


