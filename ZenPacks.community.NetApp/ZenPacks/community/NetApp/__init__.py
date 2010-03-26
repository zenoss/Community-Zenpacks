import Globals
import os.path

from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.DeviceClass import manage_addDeviceClass
from Products.ZenModel.ZenossSecurity import ZEN_VIEW

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ NetApp Storage loader
    """

    def install(self, app):
	# Device - Storage organizer
        if not hasattr(app.zport.dmd.Devices, 'Storage'):
            manage_addDeviceClass(app.zport.dmd.Devices, 'Storage')
        dc = app.zport.dmd.Devices.getOrganizer('Storage')
        dc.description = ''
	# MIB - Storage organizer
        if not hasattr(app.zport.dmd.Mibs, 'Storage'):
            manage_addDeviceClass(app.zport.dmd.Mibs, 'Storage')
        mg = app.zport.dmd.Mibs.getOrganizer('Storage')
	mg.description = ''

        ZenPackBase.install(self, app)

    def upgrade(self, app):
	# Device - Storage organizer
        if not hasattr(app.zport.dmd.Devices, 'Storage'):
            manage_addDeviceClass(app.zport.dmd.Devices, 'Storage')
        dc = app.zport.dmd.Devices.getOrganizer('Storage')
        dc.description = ''
	# MIB - Storage organizer
        if not hasattr(app.zport.dmd.Mibs, 'Storage'):
            manage_addDeviceClass(app.zport.dmd.Mibs, 'Storage')
        mg = app.zport.dmd.Mibs.getOrganizer('Storage')
	mg.description = ''

        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app, leaveObjects)

