
import Globals
import os.path
import sys

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ SQLDataSource loader
    """

    def install(self, app):
        if not hasattr(app.zport.dmd.Events.Status, 'PyDBAPI'):
            app.zport.dmd.Events.createOrganizer("/Status/PyDBAPI")
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        if not hasattr(app.zport.dmd.Events.Status, 'PyDBAPI'):
            app.zport.dmd.Events.createOrganizer("/Status/PyDBAPI")
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app, leaveObjects)
