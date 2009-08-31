import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DeviceClass import manage_addDeviceClass
from Products.ZenEvents.EventClass import manage_addEventClass

class ZenPack(ZenPackBase):
    """ IBM3584Mon ZenPack Loader
    """
    def install(self, app):
        if not hasattr(self.dmd.Events.HW.Backup, 'Tape Library'):
            manage_addEventClass(self.dmd.Events.HW.Backup, 'Tape Library')

        ZenPackBase.install(self, app)

    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app)
