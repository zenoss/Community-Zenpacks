
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenRelations.RelSchema import *
DeviceHW._relations += (("memorymodules", ToManyCont(ToOne, "ZenPacks.community.deviceAdvDetail.MemoryModule", "hw")), )
DeviceHW._relations += (("logicaldisks", ToManyCont(ToOne, "ZenPacks.community.deviceAdvDetail.LogicalDisk", "hw")), )

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
class ZenPack(ZenPackBase):
    """ Database loader
    """
    def install(self, app):
        ZenPackBase.install(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.hw.buildRelations()

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.hw.buildRelations()

    def remove(self, app, junk):
        ZenPackBase.remove(self, app, junk)
        DeviceHW._relations = tuple([x for x in DeviceHW._relations if x[0] not in ['memorymodules', 'logicaldisks']])
        for d in self.dmd.Devices.getSubDevices():
            d.hw.buildRelations()
    