
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.Device import Device

def Device_getLocationviaSNMP( self ):
    if self.location():
        return self.location().getOrganizerName()

Device.getLocationviaSNMP = Device_getLocationviaSNMP

def Device_setLocationviaSNMP( self, location ):
    self.setLocation(location)

Device.setLocationviaSNMP = Device_setLocationviaSNMP
