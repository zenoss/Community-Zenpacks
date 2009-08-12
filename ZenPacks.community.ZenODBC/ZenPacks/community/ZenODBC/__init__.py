
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
class ZenPack(ZenPackBase):
    """ ZenPack loader
    """
    def install(self, app):
        self.dmd.Events.createOrganizer("/Status/Odbc")
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        self.dmd.Events.createOrganizer("/Status/Odbc")
        ZenPackBase.upgrade(self, app)

    def remove(self, app, junk):
        ZenPackBase.remove(self, app, junk)
