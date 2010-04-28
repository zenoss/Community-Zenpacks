import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.OSX')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

class ZenPack(ZenPackBase):
    def install(self, app):
        """
        Set the collector plugins for Server/SSH/OSX.
        """
        ZenPackBase.install(self, app)
        osx = app.dmd.Devices.createOrganizer('/Server/SSH/OSX')

        plugins=[]
        plugins.append('zenoss.cmd.osx.uname_a')
        osx.setZenProperty( 'zCollectorPlugins', plugins )

