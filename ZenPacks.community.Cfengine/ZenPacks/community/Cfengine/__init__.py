import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.Cfengine')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

class ZenPack(ZenPackBase):
    packZProperties = [
        ('zCfengineComplianceFile', '/tmp/cfengine-clients.txt', 'string'),
        ]
    
    def install(self, app):
        """ 
        Cfengine device class, file location and modeling plugins
        """
        ZenPackBase.install(self, app)
        cfengine = app.dmd.Devices.createOrganizer('/Server/Cfengine')
        
        plugins=[]
        plugins.append('community.cfenginemodeler')
        cfengine.setZenProperty( 'zCollectorPlugins', plugins )
