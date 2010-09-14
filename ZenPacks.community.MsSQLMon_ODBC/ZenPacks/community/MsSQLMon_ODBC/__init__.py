
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ MsSQLMon_ODBC loader
    """
    packZProperties = [
            ('zMsSqlConnectionString', 'DRIVER={FreeTDS};TDS_Version=8.0;PORT=1433', 'string'),
            ('zMsSqlSrvInstances', '', 'string'),
            ]
