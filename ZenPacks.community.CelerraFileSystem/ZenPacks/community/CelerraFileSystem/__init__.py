import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    def install(self, app):
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app, leaveObjects)
