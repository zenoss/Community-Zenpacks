
import Globals
import os.path
from Products.ZenModel.ZenPack import ZenPackBase

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())
    



class ZenPack(ZenPackBase):
    """
    F5 BigIP Loader
    """
    
    #A List of Custom zProperties To Add
    packZProperties = [('zF5BigipVirtualServerNameFilter', '', 'string'),]
    
    def install(self, app):
        """
        F5 BigIP device class, plugins, etc
        """
        f5 = app.dmd.Devices.createOrganizer('/Network/f5')
        # Set snmp version to 2c
        f5.setZenProperty('zSnmpVer', 'v2c')
        
        # Build a list of modeler plugins that we want to apply to our new device class
        plugins=['BigipLtmVirtualServerMap', 'BigipDeviceMap']
        
        # Apply the list of plugins to the device class. This will overwrite whats there, not append
        f5.setZenProperty('zCollectorPlugins', plugins)
        
        # Register our device class file, with the new device class
        f5.setZenProperty('zPythonClass', 'ZenPacks.community.f5.BigipLtm')
        ZenPackBase.install(self, app)