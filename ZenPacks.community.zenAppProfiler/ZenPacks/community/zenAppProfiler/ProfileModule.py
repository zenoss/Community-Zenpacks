from Globals import *
from AccessControl import ClassSecurityInfo
from AccessControl import Permissions
from zope.interface import implements
from Products.ZenRelations.RelSchema import *
from Products.ZenWidgets import messaging
from Products.ZenModel.interfaces import IIndexed
from Products.ZenModel.ZenossSecurity import *
from Products.ZenModel.ZenModelRM import ZenModelRM
from Products.ZenModel.ZenPackable import ZenPackable


class ProfileModule(ZenModelRM, ZenPackable):
    """ Class ProfileModule is a container for a set of rules
    """
    implements(IIndexed)

    moduleAlerts = []
    moduleGroups = []
    moduleUsers = []
    moduleTemplates = []
    moduleGroupOrganizers = []
    moduleSystemOrganizers = []
    description = ""

    _properties = (
        {'id':'moduleGroups', 'type':'lines', 'mode':'w'},
        {'id':'moduleUsers', 'type':'lines', 'mode':'w'},
        {'id':'moduleAlerts', 'type':'lines', 'mode':'w'},
        {'id':'moduleGroupOrganizers', 'type':'lines', 'mode':'w'},
        {'id':'moduleSystemOrganizers', 'type':'lines', 'mode':'w'},
        {'id':'moduleTemplates', 'type':'lines', 'mode':'w'},
        {'id':'description', 'type':'string', 'mode':'w'},
    )

    _relations = ZenPackable._relations + (
        ("ruleorganizer", ToOne(ToManyCont, "ZenPacks.community.zenAppProfiler.ProfileOrganizer", "rulesets")),
        ("rules", ToManyCont(ToOne, "ZenPacks.community.zenAppProfiler.ProfileNode", "module")),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
        {
            'immediate_view' : 'viewProfileModule',
            'actions'        :
            (
                { 'id'            : 'profilemodule'
                , 'name'          : 'View Ruleset'
                , 'action'        : 'viewProfileModule'
                , 'permissions'   : ( Permissions.view, )
                },
                { 'id'            : 'edit'
                , 'name'          : 'Edit Ruleset'
                , 'action'        : 'editProfileModule'
                , 'permissions'   : ( Permissions.view, )
                },
            )
         },
        )

    security = ClassSecurityInfo()

    def getModuleName(self):
        """ return this module's name
        """
        return self.id

    def ruleCount(self):
        """ return number of rules
        """
        count = 0
        for rule in self.rules():
            if rule.propertyType == "System":
                continue
            if rule.propertyType == "Group":
                continue
            count += 1
        return count
    
    def getRules(self):
        """ update and return rules objects
        """
        self.createTemplateRules()
        self.createOrganizationRules()
        self.updateRuleOrganizers()
        filteredrules=[]
        for rule in self.rules():
            if rule.propertyType == "System":
                continue
            if rule.propertyType == "Group":
                continue
            filteredrules.append(rule)
        return filteredrules
    
    def getCurrentDeviceMatches(self):
        """ return list of current member devices 
            complying with a rule set
        """
        devices = []
        for rule in self.rules():
            rule.getRuleCurrentMatches()
            for d in rule.ruleCurrentMatches:
                if d not in devices:
                    devices.append(d)
        return devices
    
    def getPotentialDeviceMatches(self):
        """ return list of potential member devices 
            complying with a rule set
        """
        devices = []
        for rule in self.rules():
            rule.getRuleCurrentMatches()
            rule.getRulePotentialMatches()
            for d in rule.rulePotentialMatches:
                if d not in devices:
                    devices.append(d)
        return devices
    
    def createOrganizationRules(self):
        """ remove unneeded organization rules
        """
        self.removeOrganizationRules()
        ruleids = []
        for rule in self.rules():
            ruleids.append(rule.propertyName)
        counter = 0
        rulename = "organizer"
        for org in self.moduleGroupOrganizers:
            ruleid = rulename + '-' + str(counter)
            if org not in ruleids:
                rule = self.createRule(ruleid)
                rule.propertyType = 'Group'
                rule.propertyName = org
                rule.toRemove = False
                rule.enabled = False
                counter += 1
                
        for sys in self.moduleSystemOrganizers:
            ruleid = rulename + '-' + str(counter)
            if sys not in ruleids:
                rule = self.createRule(ruleid)
                rule.propertyType = 'System'
                rule.propertyName = sys
                rule.toRemove = False
                rule.enabled = False
                counter += 1

    def removeOrganizationRules(self):
        """ remove unneeded organization rules
        """
        ruleids = []
        for rule in self.rules():
            if rule.id.find('organizer') >=0:
                ruleids.append(rule.id)
        self.deleteRules(ruleids)
    
    def updateRuleOrganizers(self):
        ruleids = []
        """ propagate ruleset organizers to rules
        """
        for rule in self.rules():
            rule.ruleGroups = self.moduleGroupOrganizers
            rule.ruleSystems = self.moduleSystemOrganizers
    
    def getAllTemplates(self):
        """ return list of all unique templates 
        """
        self.updateRuleOrganizers()
        templates = ['']
        for t in self.dmd.Devices.getAllRRDTemplates():
            if t.id not in templates:  templates.append(t.id)
        return templates
    
 
    def createTemplateRules(self):
        """ create rules based on selected templates
        """
        self.removeTemplateRules()
        ruleids = []
        for rule in self.rules():
            ruleids.append(rule.propertyName)
        templates = self.getAllTemplates()
        rulename = "templaterule"
        counter = 0
        for t in templates:
            if t in self.moduleTemplates:
                ruleid = rulename + '-' + str(counter)
                if t not in ruleids:
                    rule = self.createRule(ruleid)
                    rule.propertyType = 'Template'
                    rule.propertyName = t
                    rule.toRemove = False
                    rule.enabled = True
                    rule.createRuleAlert()
                    counter += 1
          
    def removeTemplateRules(self):
        """ remove unneeded template rules
        """
        ruleids = []
        for rule in self.rules():
            if rule.id.find('templaterule') >=0:
                ruleids.append(rule.id)
        self.deleteRules(ruleids)
        
    def createRule(self, id, **kwargs):
        """ Create a Rule
        """
        from ProfileNode import ProfileNode
        rule = ProfileNode(id, **kwargs)
        self.rules._setObject(rule.id, rule)
        rule = self.rules._getOb(rule.id)
        rule.ruleModuleName = self.id
        rule.ruleGroups = self.moduleGroupOrganizers
        rule.ruleSystems = self.moduleSystemOrganizers
        rule.enabled = True
        return rule
    
    def addRule(self, id, REQUEST=None):
        """ Add a Rule
        """
        from ProfileNode import ProfileNode
        rule = ProfileNode(id)
        self.rules._setObject(rule.id,rule)
        rule = self.rules._getOb(id)
        rule.ruleModuleName = id
        rule.ruleGroups = self.moduleGroupOrganizers
        rule.ruleSystems = self.moduleSystemOrganizers
        
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Rule Created',
                'Rule %s was created.' % id
            )
            return self.callZenScreen(REQUEST)
        else:
            return self.rules._getOb(id)
        
    def deleteRules(self, ids=[], REQUEST=None):
        """ Delete selected rules
        """
        for rule in self.rules():
            id = getattr(rule, 'id', None)
            if id in ids:
                self.rules._delObject(id)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Rules Deleted',
                'Rules deleted: %s' % (', '.join(ids))
            )
            return self.callZenScreen(REQUEST)
    
    def getAllUserNames(self):
        """ return list of all unique templates 
        """
        users = ['']
        for u in self.dmd.ZenUsers.getAllUserSettingsNames():
            if u not in users:  users.append(u)
        return users
    
    def getAllGroupNames(self):
        """ return list of all unique templates 
        """
        groups = []
        for g in self.dmd.ZenUsers.getAllGroupSettingsNames():
            if g not in groups:  groups.append(g)
        return groups
    
    def createModuleGroup(self):
        """ create Group named after this module
            if it doesn't exist
        """
        self.moduleGroups = []
        if self.id not in self.dmd.ZenUsers.getAllGroupSettingsNames():
            self.dmd.ZenUsers.manage_addGroup(self.id)
        if self.id not in self.moduleGroups:
            self.moduleGroups.append(self.id)
        groups = []
        for g in self.moduleGroups:
            if g not in groups: groups.append(g)
        self.moduleGroups = groups

    def addModuleUsersToGroups(self):
        """ add moduleUsers to moduleGroups
        """
        for g in self.moduleGroups:
            group = self.dmd.ZenUsers.getGroupSettings(g)
            for u in self.moduleUsers:
                if u not in group.getMemberUserIds():
                    user = self.dmd.ZenUsers.getUserSettings(u)
                    group.manage_addUsersToGroup([user.id])
        self.setModuleAdminGroups()
        return self.moduleUsers

    def getModuleUserSettings(self):
        """ return Group objects for this rule set
        """
        userSettings = []
        for u in self.moduleUsers:
            settings = self.dmd.ZenUsers.getUserSettings(u)
            userSettings.append(settings)
        return userSettings
    
    def getModuleGroupSettings(self):
        """ return Group objects for this rule set
        """
        groupSettings = []
        for m in self.moduleGroups:
            settings = self.dmd.ZenUsers.getGroupSettings(m)
            if settings not in groupSettings:
                groupSettings.append(settings)
        return groupSettings

    def setModuleAdminGroups(self):
        """ build Add moduleGroups to Administrative
            Roles on Group/System Organizers
        """
        for moduleGroup in self.moduleGroups:
            usergroup = self.dmd.ZenUsers.getGroupSettings(moduleGroup)
            for group in self.moduleGroupOrganizers:
                usergroup.manage_addAdministrativeRole(group,type='group')
                usergroup.manage_editAdministrativeRoles(group,role='ZenManager',level=1)

            for system in self.moduleSystemOrganizers:
                usergroup.manage_addAdministrativeRole(system,type='system')
                usergroup.manage_editAdministrativeRoles(system,role='ZenManager',level=1)

    def setModuleAlerts(self):
        """ build self.moduleAlerts property
        """
        self.moduleAlerts = []
        for rule in self.rules():
            for alert in rule.ruleAlerts:
                if alert not in self.moduleAlerts:
                    self.moduleAlerts.append(alert)
        
    def getModuleAlertSettings(self):
        """ return alert objects for this rule set's groups
        """
        self.setModuleAlerts()
        alertSettings = []
        for group in self.getModuleGroupSettings():
            alerts = group.getActionRules()
            for alert in alerts:
                for moduleAlert in self.moduleAlerts:
                    if alert.id == moduleAlert:
                        alertSettings.append(alert)    
        return alertSettings
    
    def manage_buildModuleAlerts(self, REQUEST=None):
        """ build alert definitions based on rules
        """
        self.createModuleGroup()
        for rule in self.rules():
            alerts = rule.createRuleAlert()
            for alert in alerts:
                if alert not in self.moduleAlerts:
                    self.moduleAlerts.append(alert)
        if REQUEST:
            if alerts:
                messaging.IMessageSender(self).sendToBrowser(
                    'Alerts Built',
                    'Alerts built: %s' % self.id
                )
            return self.callZenScreen(REQUEST)

    def manage_runModuleMembershipRules(self, REQUEST=None):
        """ add memberships to devices matching ruleset rules
        """
        self.removeMembershipRules()
        rules = self.addMembershipRules()
        if REQUEST:
            if rules:
                messaging.IMessageSender(self).sendToBrowser(
                    'Memberships Modified',
                    'Memberships modified for Rulset: %s' % self.id
                )
            return self.callZenScreen(REQUEST)
        
    def addMembershipRules(self):
        """ add devices to groups if they match any rules in the ruleset
        """
        addedDevices = []
        from ProfileModify import ProfileModify
        for device in self.getPotentialDeviceMatches():
            addedDevices.append(device)
            for system in self.moduleSystemOrganizers:
                ruleApplication = ProfileModify(self.dmd,device.id,system)
                ruleApplication.addSystemToDevice()
            for group in self.moduleGroupOrganizers:
                ruleApplication = ProfileModify(self.dmd,device.id,group)
                ruleApplication.addGroupToDevice()
        return addedDevices
        
    def removeMembershipRules(self):
        """ remove devices from rules if the toRemove flag is True
            for a given rule
        """
        from ProfileModify import ProfileModify
        removedDevices = []
        for rule in self.rules():
            if rule.toRemove == True:
                for device in self.dmd.Devices.getSubDevices():
                    remove = False
                    if device not in rule.ruleCurrentMatches:
                        remove = True
                    elif device not in rule.rulePotentialMatches:
                        remove = True
                    if remove == True:
                        removedDevices.append(device)
                        for system in self.moduleSystemOrganizers:
                            ruleApplication = ProfileModify(self.dmd,device.id,system)
                            ruleApplication.removeSystemFromDevice()
                        for group in self.moduleGroupOrganizers:
                            ruleApplication = ProfileModify(self.dmd,device.id,group)
                            ruleApplication.removeGroupFromDevice()
        return removedDevices
 
InitializeClass(ProfileModule)
