
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

import ZenPacks.DrD_Studios.BlueArc
def initialize(registrar):
    registrar.registerClass(
          ClusterNode.ClusterNode,
          permission='Add DMD Objects',
    )
