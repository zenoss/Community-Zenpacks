import Globals
import os.path

from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.ZenossSecurity import ZEN_VIEW

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())


