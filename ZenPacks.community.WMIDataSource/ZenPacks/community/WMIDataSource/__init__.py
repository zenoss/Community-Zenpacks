
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ WMIDataSource loader
    """
    packZProperties = [
            ('zWmiProxy', '', 'string'),
            ]

    def install(self, app):
        if not hasattr(app.zport.dmd.Events.Status, 'Wbem'):
            app.zport.dmd.Events.createOrganizer("/Status/Wbem")
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        if not hasattr(app.zport.dmd.Events.Status, 'Wbem'):
            app.zport.dmd.Events.createOrganizer("/Status/Wbem")
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app, leaveObjects)
