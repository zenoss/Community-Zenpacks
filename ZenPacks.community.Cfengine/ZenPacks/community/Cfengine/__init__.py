import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase
from Products.CMFCore.DirectoryView import registerDirectory

log = logging.getLogger('zen.Cfengine')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

class ZenPack(ZenPackBase):
    """ Cfengine loader
    """

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
        server = app.dmd.findChild('Devices/Server')
        for plugin in server.zCollectorPlugins:
            plugins.append(plugin)

        plugins.append('community.cfenginemodeler')

        cfengine.setZenProperty( 'zCollectorPlugins', plugins )
