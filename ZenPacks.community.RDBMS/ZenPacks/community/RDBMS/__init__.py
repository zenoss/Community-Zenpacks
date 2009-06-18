
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenUtils.Utils import prepId
from Database import manage_addDatabase



def addDatabase(self, id, userCreated, REQUEST=None):
    """Add a Database.
    """
    dbid = prepId(id)
    manage_addDatabase(self.softwaredatabases, id, userCreated)
    self._p_changed = True
    if REQUEST:
        REQUEST['message'] = 'Database created'
        REQUEST['RESPONSE'].redirect(
            self.softwaredatabases._getOb(dbid).absolute_url())
        return self.callZenScreen(REQUEST)
            
def deleteDatabases(self, componentNames=[], REQUEST=None):
    """Delete Databases"""
    self.deleteDeviceComponents(self.softwaredatabases, componentNames, REQUEST)
    if REQUEST: 
        REQUEST['message'] = 'Database deleted'
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)
    
def unlockDatabases(self, componentNames=[], REQUEST=None):
    """Unlock Databases"""
    self.unlockDeviceComponents(self.softwaredatabases, componentNames, REQUEST)
    if REQUEST: 
        REQUEST['message'] = 'Databases unlocked'
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)
        
def lockDatabasesFromDeletion(self, componentNames=[], 
        sendEventWhenBlocked=None, REQUEST=None):
    """Lock FileSystems from deletion"""
    self.lockDeviceComponentsFromDeletion(self.softwaredatabases, componentNames, 
        sendEventWhenBlocked, REQUEST)
    if REQUEST: 
        REQUEST['message'] = 'Databases locked from deletion'
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)
    
def lockDatabasesFromUpdates(self, componentNames=[], 
        sendEventWhenBlocked=None, REQUEST=None):
    """Lock Databases from updates"""
    self.lockDeviceComponentsFromUpdates(self.softwaredatabases, componentNames, 
        sendEventWhenBlocked, REQUEST)
    if REQUEST: 
        REQUEST['message'] = 'Databases locked from updates and deletion'
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenRelations.RelSchema import *
OperatingSystem._relations += (("softwaredatabases", ToManyCont(ToOne, "ZenPacks.community.RDBMS.Database", "os")), )
OperatingSystem.addDatabase = addDatabase
OperatingSystem.deleteDatabases = deleteDatabases
OperatingSystem.unlockDatabases = unlockDatabases
OperatingSystem.lockDatabasesFromDeletion = lockDatabasesFromDeletion
OperatingSystem.lockDatabasesFromUpdates = lockDatabasesFromUpdates

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
class ZenPack(ZenPackBase):
    """ Database loader
    """
    
    def install(self, app):
        if hasattr(self.dmd.zenMenus, 'Database'):
            self.dmd.zenMenus._delObject('Database')
        self.dmd.zenMenus.manage_addZenMenu('Database')
        ZenPackBase.install(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

    def upgrade(self, app):
        if hasattr(self.dmd.zenMenus, 'Database'):
            self.dmd.zenMenus._delObject('Database')
        self.dmd.zenMenus.manage_addZenMenu('Database')
        ZenPackBase.upgrade(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

    def remove(self, app, junk):
        ZenPackBase.remove(self, app, junk)
        if hasattr(self.dmd.zenMenus, 'Database'):
            self.dmd.zenMenus._delObject('Database')
        OperatingSystem._relations = tuple([x for x in OperatingSystem._relations if x[0] != 'softwaredatabases'])
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()


    