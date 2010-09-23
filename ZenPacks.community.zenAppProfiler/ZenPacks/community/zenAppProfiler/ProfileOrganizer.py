import types
from Globals import *
from AccessControl import ClassSecurityInfo
from AccessControl import Permissions
from Products.ZenModel.ZenossSecurity import *
from Products.ZenModel.Organizer import Organizer
from Products.ZenRelations.RelSchema import *
from Products.ZenUtils.Search import makeCaseInsensitiveKeywordIndex
from Products.ZenWidgets import messaging
from Products.ZenModel.ZenPackable import ZenPackable

def manage_addProfileOrganizer(context, id='Profiles', REQUEST = None):
    """make a device class"""
    porg = ProfileOrganizer(id)
    context._setObject(id, porg)
    porg = context._getOb(id)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url() + '/manage_main')
        
addProfileOrganizer = DTMLFile('dtml/addProfileOrganizer',globals())


class ProfileOrganizer(Organizer, ZenPackable):
    """
    ProfileOrganizer is the base class for rulesets and rules
    """
    meta_type = "ProfileOrganizer"
    dmdRootName = "Profiles"
    default_catalog = 'profileSearch'
    
    security = ClassSecurityInfo()

    _relations = Organizer._relations + ZenPackable._relations + (
        ("rulesets", ToManyCont(ToOne,"ZenPacks.community.zenAppProfiler.ProfileModule","ruleorganizer")),
        )

    factory_type_information = (
        {
            'immediate_view' : 'viewProfileOrganizer',
            'actions'        :
            (
                { 'id'            : 'settings'
                , 'name'          : 'Settings'
                , 'action'        : 'editSettings'
                , 'permissions'   : ('Manage DMD',)
                },
                { 'id'            : 'manage'
                , 'name'          : 'Commands'
                , 'action'        : 'dataRootManage'
                , 'permissions'   : ('Manage DMD',)
                },
                { 'id'            : 'users'
                , 'name'          : 'Users'
                , 'action'        : 'ZenUsers/manageUserFolder'
                , 'permissions'   : ('Manage DMD',)
                },
                { 'id'            : 'packs'
                , 'name'          : 'ZenPacks'
                , 'action'        : 'ZenUsers/manageUserFolder'
                , 'permissions'   : ('Manage DMD',)
                },
                { 'id'            : 'jobs'
                , 'name'          : 'Jobs'
                , 'action'        : 'joblist'
                , 'permissions'   : ('Manage DMD',)
                },
                { 'id'            : 'portlets'
                , 'name'          : 'Portlets'
                , 'action'        : 'editPortletPerms'
                , 'permissions'   : ('Manage DMD',)
                },
                { 'id'            : 'daemons'
                , 'name'          : 'Daemons'
                , 'action'        : '../About/zenossInfo'
                , 'permissions'   : ('Manage DMD',)
                },
                { 'id'            : 'versions'
                , 'name'          : 'Versions'
                , 'action'        : '../About/zenossVersions'
                , 'permissions'   : ('Manage DMD',)
                },
                { 'id'            : 'backups'
                , 'name'          : 'Backups'
                , 'action'        : 'backupInfo'
                , 'permissions'   : ('Manage DMD',)
                },
                { 'id'            : 'profileorganizer'
                , 'name'          : 'Profiles'
                , 'action'        : 'viewProfileOrganizer'
                , 'permissions'   : ('Manage DMD',)
                },
            )

         },
        )
    
    def __init__(self, id=None):
        if not id: id = self.dmdRootName
        super(ProfileOrganizer, self).__init__(id)
        if self.id == self.dmdRootName:
            self.createCatalog()
            
    def manage_runMembershipRulesOld(self, REQUEST=None):
        """ add memberships to devices matching all
            ruleset rules
        """
        from ProfileJob import manage_ModifyAllMemberships
        rules = manage_ModifyAllMemberships(self.dmd)
        if REQUEST:
            if rules:
                messaging.IMessageSender(self).sendToBrowser(
                    'Membership Jobs Submitted',
                    'membership jobs submitted: %s' % self.id
                )
            return self.callZenScreen(REQUEST)
        
    def manage_runMembershipRules(self, REQUEST=None):
        """ add memberships to devices matching all
            ruleset rules
        """
        modified = []
        for ruleset in self.rulesets():
                ruleset.removeMembershipRules()
                rules = ruleset.addMembershipRules()
                if rules:
                    modified.append(ruleset.id)
        if REQUEST:
            if modified:
                messaging.IMessageSender(self).sendToBrowser(
                    'Memberships Modified',
                    'membership modified for rulsets: %s' % modified
                )
            return self.callZenScreen(REQUEST)
                
    def countClasses(self):
        """ Count all rulesets with in a ProfileOrganizer.
        """
        count = self.rulesets.countObjects()
        for group in self.children():
            count += group.countClasses()
        return count

    def createProfileModule(self, name, path="/"):
        """ Create a rule set
        """
        profiles = self.getDmdRoot(self.dmdRootName)
        mod = None
        if not mod:
            modorg = profiles.createOrganizer(path)
            from ProfileModule import ProfileModule
            mod = ProfileModule(name)
            modorg.rulesets._setObject(mod.id, mod)
            mod = modorg.rulesets._getOb(mod.id)
            mod.createModuleGroup()
        return mod
    
    def manage_addProfileModule(self, id, REQUEST=None):
        """ Create a new service class in this Organizer.
        """
        from ProfileModule import ProfileModule
        module = ProfileModule(id)
        self.rulesets._setObject(id, module)
        mod = self.rulesets._getOb(module.id)
        mod.createModuleGroup()
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Rule Set Created',
                'rule set %s was created.' % id
            )
            return self.callZenScreen(REQUEST)
        else:
            return self.rulesets._getOb(id)
        
    def removeProfileModules(self, ids=None, REQUEST=None):
        """ Remove Profile Modules from an EventClass.
        """
        if not ids: return self()
        if type(ids) == types.StringType: ids = (ids,)
        for id in ids:
            self.rulesets._delObject(id)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Rule Sets Deleted',
                'rule sets deleted: %s' % ', '.join(ids)
            )
            return self()
        
    def moveProfileModules(self, moveTarget, ids=None, REQUEST=None):
        """Move ProfileModules from this EventClass to moveTarget.
        """
        if not moveTarget or not ids: return self()
        if type(ids) == types.StringType: ids = (ids,)
        target = self.getChildMoveTarget(moveTarget)
        for id in ids:
            rec = self.rulesets._getOb(id)
            rec._operation = 1 # moving object state
            self.rulesets._delObject(id)
            target.rulesets._setObject(id, rec)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Rule Set Moved',
                'rule set moved to %s.' % moveTarget
            )
            REQUEST['RESPONSE'].redirect(target.getPrimaryUrlPath())

    def reIndex(self):
        print "reIndex"
        """Go through all devices in this tree and reindex them."""
        zcat = self._getOb(self.default_catalog)
        zcat.manage_catalogClear()
        for org in [self,] + self.getSubOrganizers():
            for ruleset in org.rulesets():
                for thing in ruleset.rules():
                    thing.index_object()

    def createCatalog(self):
        """Create a catalog for rules searching"""
        from Products.ZCatalog.ZCatalog import manage_addZCatalog
        # XXX update to use ManagableIndex
        manage_addZCatalog(self, self.default_catalog, self.default_catalog)
        zcat = self._getOb(self.default_catalog)
        cat = zcat._catalog
        cat.addIndex('ruleSystems', makeCaseInsensitiveKeywordIndex('ruleSystems'))
        cat.addIndex('ruleGroups', makeCaseInsensitiveKeywordIndex('ruleGroups'))
        cat.addIndex('propertyType', makeCaseInsensitiveKeywordIndex('propertyType'))
        cat.addIndex('propertyName', makeCaseInsensitiveKeywordIndex('propertyName'))
        zcat.addColumn('toRemove')
        zcat.addColumn('enabled')
        zcat.addColumn('ruleModuleName')

InitializeClass(ProfileOrganizer)

