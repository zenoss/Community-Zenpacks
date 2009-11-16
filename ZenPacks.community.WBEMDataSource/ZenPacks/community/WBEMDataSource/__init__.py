
import Globals
import os.path
import sys

from Products.CMFCore.DirectoryView import registerDirectory
skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())
libDir = os.path.join(os.path.dirname(__file__), 'lib')
if os.path.isdir(libDir):
#    registerDirectory(libDir, globals())
    sys.path.append(libDir)

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ WBEMDataSource loader
    """
    packZProperties = [
            ('zWbemPort', '5989', 'string'),
            ('zWbemProxy', '', 'string'),
            ('zWbemUseSSL', 'True', 'boolean'),
	    ]

    def install(self, app):
        self.dmd.Events.createOrganizer("/Status/Wbem")
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        self.dmd.Events.createOrganizer("/Status/Wbem")
        ZenPackBase.upgrade(self, app)

    def remove(self, app, junk):
        ZenPackBase.remove(self, app, junk)
