
__doc__="ZXTM Load Balancer Zen Pack"

import Globals
import os

from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.DeviceClass import manage_addDeviceClass

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

import ZenPacks.community.ZeusLoadBalancer
def initialize(registrar):
    registrar.registerClass(
    ZeusPool.ZeusPool,
    permission='Add DMD Objects',
    )


class ZenPack(ZenPackBase):
    """ Zeus loader
    """

    def install(self, app):
        if not hasattr(app.zport.dmd.Devices.Server, 'Zeus'):
            manage_addDeviceClass(app.zport.dmd.Devices.Server, 'Zeus')
        dc = app.zport.dmd.Devices.getOrganizer('Server/Zeus')
        dc.description = 'Zeus Load Balancers'
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        if not hasattr(app.zport.dmd.Devices.Server, 'Zeus'):
            manage_addDeviceClass(app.zport.dmd.Devices.Server, 'Zeus')
        dc = app.zport.dmd.Devices.getOrganizer('Server/Zeus')
        dc.description = 'Zeus Load Balancers'
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        ZenPackBase.remove(self, app, leaveObjects)
