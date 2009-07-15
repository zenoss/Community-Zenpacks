import Globals
from Products.ZenModel.migrate.Migrate import Version
from ZenPacks.community.CeleraFileSystem import ZenPack

class BaseClass:
    version = Version(2, 0, 0)

    def migrate(self, pack):
        if pack.__class__ != ZenPack:
            pack.__class__ = ZenPack

