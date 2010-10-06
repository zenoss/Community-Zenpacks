import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

import transaction
from Products.ZenModel.ZenossInfo import ZenossInfo
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.ZenMenu import ZenMenu

class ZenPack(ZenPackBase):
    """ ZenPack loader
    """
    
    profilerTab = { 'id'            : 'profileorganizer'
                   , 'name'          : 'Profiles'
                   , 'action'        : 'Profiles/viewProfileOrganizer'
                   , 'permissions'   : ( "Manage DMD", )
                   }

    def addProfilerTab(self,app):
        dmdloc = self.dmd
        finfo = dmdloc.factory_type_information
        actions = list(finfo[0]['actions'])
        for i in range(len(actions)):
            if (self.profilerTab['id'] in actions[i].values()):
                return
        actions.append(self.profilerTab)
        finfo[0]['actions'] = tuple(actions)
        dmdloc.factory_type_information = finfo
        transaction.commit()
    
    def rmvProfilerTab(self,app):
        dmdloc = self.dmd
        finfo = dmdloc.factory_type_information
        actions = list(finfo[0]['actions'])
        for i in range(len(actions)):
            if (self.profilerTab['id'] in actions[i].values()):
                actions.remove(self.profilerTab)
        finfo[0]['actions'] = tuple(actions)
        dmdloc.factory_type_information = finfo
        transaction.commit()
    
    def installMenus(self,app):
        dmdloc = self.dmd
        self.removeMenus(dmdloc)

        modulemenu = ZenMenu('ModuleMenu')
        dmdloc.zenMenus._setObject(modulemenu.id, modulemenu)
        modulemenu = dmdloc.zenMenus._getOb(modulemenu.id)
        modulemenu.manage_addZenMenuItem('addModule',
                                   action='dialog_addModule',  # page template that is called
                                   description='Add Ruleset',
                                   ordering=4.0,
                                   isdialog=True)
        modulemenu.manage_addZenMenuItem('removeModule',
                                   action='dialog_removeModule',  # page template that is called
                                   description='Remove Ruleset',
                                   ordering=3.0,
                                   isdialog=True)
        modulemenu.manage_addZenMenuItem('runAllMembershipRules',
                                   action='dialog_runAllMembershipRules',  # page template that is called
                                   description='Build All Memberships',
                                   ordering=2.0,
                                   isdialog=True)
        
        modulemenu = ZenMenu('RuleDefinitions')
        dmdloc.zenMenus._setObject(modulemenu.id, modulemenu)
        modulemenu = dmdloc.zenMenus._getOb(modulemenu.id)
        modulemenu.manage_addZenMenuItem('addRule',
                                   action='dialog_addRule',  # page template that is called
                                   description='Add Rule',
                                   ordering=4.0,
                                   isdialog=True)
        modulemenu.manage_addZenMenuItem('removeRule',
                                   action='dialog_removeRule',  # page template that is called
                                   description='Remove Rule',
                                   ordering=3.0,
                                   isdialog=True)
        
        modulemenu = ZenMenu('RuleModule')
        dmdloc.zenMenus._setObject(modulemenu.id, modulemenu)
        modulemenu = dmdloc.zenMenus._getOb(modulemenu.id)
        modulemenu.manage_addZenMenuItem('runAllMembershipRules',
                                   action='dialog_runModuleMembershipRules',  # page template that is called
                                   description='Build Memberships',
                                   ordering=2.0,
                                   isdialog=True)
        modulemenu.manage_addZenMenuItem('buildAlerts',
                                   action='dialog_buildModuleAlerts',  # page template that is called
                                   description='Build Alerts',
                                   ordering=1.0,
                                   isdialog=True)
        
           
    def removeMenus(self, dmd):
        try:
            self.dmd.zenMenus._delObject('ModuleMenu')
        except AttributeError:
            pass
        try:
            self.dmd.zenMenus._delObject('RuleDefinitions')
        except AttributeError:
            pass
        try:
            self.dmd.zenMenus._delObject('RuleModule')
        except AttributeError:
            pass

    def install(self, app):
        ZenPackBase.install(self, app)
        self.addProfilerTab(app)
        self.installMenus(app.zport.dmd)
        
    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self.addProfilerTab(app)
        self.installMenus(app.zport.dmd)

    def remove(self, app, junk):
        self.rmvProfilerTab(app)
        self.dmd._delObject('Profiles')
        self.removeMenus(self.zport.dmd)
        #ZenPackBase.remove(self, app, junk)
        #ZenPackBase.remove(self.app, leaveObjects)

