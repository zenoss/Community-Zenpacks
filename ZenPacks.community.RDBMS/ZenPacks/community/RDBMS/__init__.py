
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenUtils.Utils import prepId
from Products.ZenWidgets import messaging
from Database import manage_addDatabase
from DBSrvInst import manage_addDBSrvInst

def addDatabase(self, id, userCreated, REQUEST=None):
    """Add a Database.
    """
    dbid = prepId(id)
    manage_addDatabase(self.softwaredatabases, id, userCreated)
    self._p_changed = True
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Database Created',
            'Database %s was created.' % id
        )
        REQUEST['RESPONSE'].redirect(
            self.softwaredatabases._getOb(dbid).absolute_url())
        return self.callZenScreen(REQUEST)

def deleteDatabases(self, componentNames=[], REQUEST=None):
    """Delete Databases"""
    self.deleteDeviceComponents(self.softwaredatabases, componentNames, REQUEST)
    if REQUEST: 
        messaging.IMessageSender(self).sendToBrowser(
            'Databases Deleted',
            'Databases %s were deleted.' % (', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

def unlockDatabases(self, componentNames=[], REQUEST=None):
    """Unlock Databases"""
    self.unlockDeviceComponents(self.softwaredatabases, componentNames, REQUEST)
    if REQUEST: 
        messaging.IMessageSender(self).sendToBrowser(
            'Databases Unlocked',
            'Databases %s were unlocked.' % (', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

def lockDatabasesFromDeletion(self, componentNames=[], 
        sendEventWhenBlocked=None, REQUEST=None):
    """Lock Databases from deletion"""
    self.lockDeviceComponentsFromDeletion(self.softwaredatabases, componentNames, 
        sendEventWhenBlocked, REQUEST)
    if REQUEST: 
        messaging.IMessageSender(self).sendToBrowser(
            'Databases Locked',
            'Databases %s were locked from deletion.' % (
                ', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

def lockDatabasesFromUpdates(self, componentNames=[], 
        sendEventWhenBlocked=None, REQUEST=None):
    """Lock Databases from updates"""
    self.lockDeviceComponentsFromUpdates(self.softwaredatabases, componentNames, 
        sendEventWhenBlocked, REQUEST)
    if REQUEST: 
        messaging.IMessageSender(self).sendToBrowser(
            'Databases Locked',
            'Databases %s were locked from updates and deletion.' % (
                ', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

def addDBSrvInst(self, id, userCreated, REQUEST=None):
    """Add a DBSrvInst.
    """
    dbsiid = prepId(id)
    manage_addDBSrvInst(self.softwaredbsrvinstances, id, userCreated)
    self._p_changed = True
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Database Server Instance Created',
            'Database Server Instance %s was created.' % id
        )
        REQUEST['RESPONSE'].redirect(
            self.softwaredatabases._getOb(dbid).absolute_url())
        return self.callZenScreen(REQUEST)

def deleteDBSrvInsts(self, componentNames=[], REQUEST=None):
    """Delete DBSrvInsts"""
#    databases = []
#    for dbsi in self.softwaredbsrvinstances():
#       if dbsi.id not in componentNames: continue
#       databases.extend(db.id for db in dbsi.databases())
#    if databases:
#        self.deleteDeviceComponents(self.softwaredatabases, databases, None)
    self.deleteDeviceComponents(self.softwaredbsrvinstances, componentNames, REQUEST)
    if REQUEST: 
        messaging.IMessageSender(self).sendToBrowser(
            'Database Server Instances Deleted',
            'Database Server Instances %s were deleted.' % (', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

def unlockDBSrvInsts(self, componentNames=[], REQUEST=None):
    """Unlock DBSrvInsts"""
    self.unlockDeviceComponents(self.softwaredbsrvinstances, componentNames, REQUEST)
    if REQUEST: 
        messaging.IMessageSender(self).sendToBrowser(
            'Database Server Instances Unlocked',
            'Database Server Instances %s were unlocked.' % (', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

def lockDBSrvInstsFromDeletion(self, componentNames=[], 
        sendEventWhenBlocked=None, REQUEST=None):
    """Lock DBSrvInsts from deletion"""
    self.lockDeviceComponentsFromDeletion(self.softwaredbsrvinstances, componentNames, 
        sendEventWhenBlocked, REQUEST)
    if REQUEST: 
        messaging.IMessageSender(self).sendToBrowser(
            'Database Server Instances Locked',
            'Database Server Instances %s were locked from deletion.' % (
                ', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

def lockDBSrvInstsFromUpdates(self, componentNames=[], 
        sendEventWhenBlocked=None, REQUEST=None):
    """Lock DBSrvInsts from updates"""
    self.lockDeviceComponentsFromUpdates(self.softwaredbsrvinstances, componentNames, 
        sendEventWhenBlocked, REQUEST)
    if REQUEST: 
        messaging.IMessageSender(self).sendToBrowser(
            'Database Server Instances Locked',
            'Database Server Instances %s were locked from updates and deletion.' % (
                ', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenRelations.RelSchema import *
OperatingSystem._relations += (("softwaredatabases", ToManyCont(ToOne,
                                    "ZenPacks.community.RDBMS.Database", "os")),
                                ("softwaredbsrvinstances", ToManyCont(ToOne,
				    "ZenPacks.community.RDBMS.DBSrvInst", "os")),
			    )
OperatingSystem.addDatabase = addDatabase
OperatingSystem.deleteDatabases = deleteDatabases
OperatingSystem.unlockDatabases = unlockDatabases
OperatingSystem.lockDatabasesFromDeletion = lockDatabasesFromDeletion
OperatingSystem.lockDatabasesFromUpdates = lockDatabasesFromUpdates
OperatingSystem.addDBSrvInst = addDBSrvInst
OperatingSystem.deleteDBSrvInsts = deleteDBSrvInsts
OperatingSystem.unlockDBSrvInsts = unlockDBSrvInsts
OperatingSystem.lockDBSrvInstsFromDeletion = lockDBSrvInstsFromDeletion
OperatingSystem.lockDBSrvInstsFromUpdates = lockDBSrvInstsFromUpdates

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
class ZenPack(ZenPackBase):
    """ Database loader
    """

    def _removeMenu(self, menuName):
	zm = getattr(self.dmd.zenMenus, menuName, None)
	if not zm: return
	for mi in zm.zenMenuItems():
	    zm.zenMenuItems._delObject(mi.id)
        self.dmd.zenMenus._delObject(menuName)

    def _addMenu(self, mN, mD):
	if hasattr(self.dmd.zenMenus, mN): self._removeMenu(mN)
        self.dmd.zenMenus.manage_addZenMenu(mN)
	zm = getattr(self.dmd.zenMenus, mN)
	miparams = (('add%s'%mN, 'Add %s...'%mN, 'dialod_add%s'%mN, 90.0),
	        ('delete%ss'%mN, 'Delete %s...'%mN, 'dialod_delete%ss'%mN, 80.0),
	        ('lock%ss'%mN, 'Lock %s...'%mN, 'dialod_lock%ss'%mN, 70.0),
	        ('changeMonitoring', 'Monitoring...', 'dialod_changeMonitoring', 0.0))
	for param in miparams:
            zm.manage_addZenMenuItem(id=param[0],
	                            description=param[1],
				    action=param[2], 
                                    permissions=('View',),
				    isdialog=True,
				    isglobal=True, 
	                            ordering=param[3])

    def install(self, app):
        self._removeMenu('Database')
        self._addMenu('Database', 'Database')
        self._removeMenu('DBSrvInst')
        self._addMenu('DBSrvInst', 'Database Server Instance')
        ZenPackBase.install(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self._removeMenu('Database')
        self._addMenu('Database', 'Database')
        self._removeMenu('DBSrvInst')
        self._addMenu('DBSrvInst', 'Database Server Instance')
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

    def remove(self, app, junk):
        self._removeMenu('Database')
        self._removeMenu('DBSrvInst')
        ZenPackBase.remove(self, app, junk)
        OperatingSystem._relations = tuple([x for x in OperatingSystem._relations if x[0] not in ('softwaredatabases','softwaredbsrvinstances')])
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()


    