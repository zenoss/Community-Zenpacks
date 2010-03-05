
__doc__="HP Blade Chassis Zen Pack"

import Globals
import os

from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.DeviceClass import manage_addDeviceClass

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


class ZenPack(ZenPackBase):
    """ HPBladeChassis loader
    """

    def install(self, app):
        if not hasattr(app.zport.dmd.Devices, 'BladeChassis'):
            manage_addDeviceClass(app.zport.dmd.Devices, 'BladeChassis')
        dc = app.zport.dmd.Devices.getOrganizer('BladeChassis')
        dc.description = ''
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        if not hasattr(app.zport.dmd.Devices, 'BladeChassis'):
            manage_addDeviceClass(app.zport.dmd.Devices, 'BladeChassis')
        dc = app.zport.dmd.Devices.getOrganizer('BladeChassis')
        dc.description = ''
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app, leaveObjects)

