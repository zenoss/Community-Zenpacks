
import Globals
import os.path
from Products.CMFCore.DirectoryView import registerDirectory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
class ZenPack(ZenPackBase):
    """ ZenPacks.altea.SQLServer loader
    """

    packZProperties = [
            ('zSQLInstance', 'SQLSERVER', 'string'),
        ]
