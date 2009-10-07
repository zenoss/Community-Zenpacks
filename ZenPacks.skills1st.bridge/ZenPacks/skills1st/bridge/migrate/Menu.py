#
# This class is only needed if you have a menu item instead of a tab (or both). 
#If you just use a tab then you can delete this before installing your zenpack
#
import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPack

class Menu:
    version = Version(1, 0, 0)

    def migrate(self, pack):
        dmd = pack.__primary_parent__.__primary_parent__
        id = 'BridgeDeviceDetail'
        try:
            dmd.zenMenus.More.manage_deleteZenMenuItem((id,))
        except (KeyError, AttributeError):
            pass
        dmd.zenMenus.More.manage_addZenMenuItem(
            id,
            action=id,
            description='Bridge Devices',
            allowed_classes=('BridgeDevice',),
            ordering=5.0)

Menu()
