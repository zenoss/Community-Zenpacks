import Globals
from zope.interface import implements
from Products.ZenModel.ZenModelRM import ZenModelRM
from Products.ZenModel.ZenPackable import ZenPackable
from Products.ZenModel.interfaces import IIndexed
from Products.ZenRelations.RelSchema import *
from AccessControl import Permissions
from Products.ZenModel.ZenossSecurity import *
from ProfileModule import ProfileModule


class ProfileNode(ZenModelRM, ZenPackable):
    """ Class ProfileNode defines the rule and
        its properties
    """
    implements(IIndexed)
    default_catalog = 'profileSearch'

    ruleSystems = []
    ruleGroups = []
    propertyType = ""
    propertyName = ""
    toRemove = False
    enabled = False
    ruleAlerts = []
    ruleModuleName = ""
    ruleCurrentMatches = []
    rulePotentialMatches = []

    _properties = (
        {'id':'ruleSystems', 'type':'lines', 'mode':'w'},
        {'id':'ruleGroups', 'type':'lines', 'mode':'w'},
        {'id':'propertyType', 'type':'string', 'mode':'w',},
        {'id':'propertyName', 'type':'string', 'mode':'w'},
        {'id':'toRemove', 'type':'boolean', 'mode':'w'},
        {'id':'enabled', 'type':'boolean', 'mode':'w'},
        {'id':'ruleAlerts', 'type':'lines', 'mode':'w'},
        {'id':'ruleModuleName', 'type':'string', 'mode':'w'},
        {'id':'ruleCurrentMatches', 'type':'lines', 'mode':'w'},
        {'id':'rulePotentialMatches', 'type':'lines', 'mode':'w'},
    )

    _relations = ZenPackable._relations[:] + (
        ("module", ToOne(ToManyCont, "ZenPacks.community.zenAppProfiler.ProfileModule", "rules")),
    )

    factory_type_information = (
        {
            'immediate_view' : 'viewProfileNode',
            'actions'        :
            (
                { 'id'            : 'profilenode'
                , 'name'          : 'View Rule'
                , 'action'        : 'viewProfileNode'
                , 'permissions'   : ( Permissions.view, )
                },
                { 'id'            : 'edit'
                , 'name'          : 'Edit Rule'
                , 'action'        : 'editProfileNode'
                , 'permissions'   : ( Permissions.view, )
                },
            )
         },
        )
    
    def __init__(self, id, title="", **kwargs):
        super(ZenModelRM, self).__init__(id, title)
        atts = self.propertyIds()
        for key, val in kwargs.items():
            if key in atts: setattr(self, key, val)

    def getRuleMatches(self):
        """ find potential matches for this rule:
        """
        self.rulePotentialMatches = []
        self.ruleCurrentMatches = []
        for device in self.dmd.Devices.getSubDevices():
            potential = False
            current = False
            if self.propertyType == "System":
                continue
            if self.propertyType == "Group":
                continue
            if self.propertyType == 'Template':
                if self.findTemplateOnDevice(device) == True:
                    potential = True
            if self.findComponentMetaTypeOnDevice(device) == True:
                    potential = True
            if potential == True:
                sysresult = self.findSystemMembers(device)
                grpresult = self.findGroupMembers(device)
                if sysresult == True and grpresult == True:
                    current = True
                    potential = False
            if potential == True:
                if device not in self.rulePotentialMatches:
                    self.rulePotentialMatches.append(device)
            if current == True:
                if device not in self.ruleCurrentMatches:
                    self.ruleCurrentMatches.append(device)  

    def getRulePotentialMatches(self):
        """ find potential matches for this rule:
        """
        self.getRuleMatches()
        return self.rulePotentialMatches
    
    def getRuleCurrentMatches(self):
        """ find current rule matches that are 
            already members of groups
        """
        self.getRuleMatches()
        return self.ruleCurrentMatches
        
    def getAllTemplates(self):
        """ return list of all unique templates 
        """
        templates = ['']
        for t in self.dmd.Devices.getAllRRDTemplates():
            if t.id not in templates:  templates.append(t.id)
        return templates
    
    def getAllComponentMetaTypes(self):
        """ return list of all unique component meta types 
        """
        metaTypeIndex = self.dmd.Devices.componentSearch.index_objects()[1]
        comptypes = []
        for mtype in metaTypeIndex.uniqueValues():
            comptypes.append(mtype.title())
        return comptypes
    
    def findComponentMetaTypeOnDevice(self,device):
        """ return True if a device component uses a given 
            component template
        """
        for component in device.getDeviceComponents():
            corrected_meta_type = component.meta_type.lower().capitalize()
            if corrected_meta_type == self.propertyType:
                if component.name().find(self.propertyName) >= 0:
                    return True
        return False
  
    def findTemplateOnDevice(self,device):
        """ return True if a template is used by a device
        """
        templates = device.zDeviceTemplates
        for template in templates:
            if template.find(self.propertyName) >=0:
                return True
        for component in device.getDeviceComponents():
            template = component.getRRDTemplateName()
            if template.find(self.propertyName) >=0:
                return True
        return False

    def findSystemMembers(self,device):
        """ find members of System organizers
        """            
        systems = device.getSystemNames()     
        for sys in self.module.moduleSystemOrganizers:
            if sys not in systems:
                return False
        return True
    
    def findGroupMembers(self,device):
        """ find members of Group organizers
        """
        groups = device.getDeviceGroupNames()     
        for grp in self.module.moduleGroupOrganizers:
            if grp not in groups:
                return False
        return True

    def getRuleTypes(self):
        """ return list of supported rule types
        """
        ruletypes = self.getAllComponentMetaTypes()
        return ruletypes
    
    def createRuleAlert(self):
        """ create alert definitions for this rule
        """
        #self.ruleAlerts = []
        if self.enabled == True:
            if self.propertyType != 'Template':
                for group in self.module.moduleGroups:
                    alertName = self.buildAlertName(group)
                    alertGroup = group
                    alertWhere = self.buildAlertWhere()
                    self.buildAlert(alertName, alertGroup, alertWhere)
                    if alertName not in self.ruleAlerts:
                        self.ruleAlerts.append(alertName)
            else:
                counter = 0
                uniqs = []
                for template in self.dmd.Devices.getAllRRDTemplates():
                    if template.id.find(self.propertyName) >=0:
                        for ds in template.getRRDDataSources():
                            if ds.eventClass not in uniqs:
                                for group in self.module.moduleGroups:
                                    alertName = self.buildAlertName(group) + '-' + ds.id + '-' + str(counter)
                                    alertGroup = group
                                    alertWhere = self.buildAlertWhere() + ' and (eventClass like \''+ ds.eventClass + '%\')'
                                    print alertName, alertGroup, alertWhere
                                    self.buildAlert(alertName, alertGroup, alertWhere)
                                    if alertName not in self.ruleAlerts:
                                        self.ruleAlerts.append(alertName)
                                counter += 1
                            uniqs.append(ds.eventClass)
        return self.ruleAlerts

    def buildAlert(self,alertName,alertGroup,alertWhere):
        """ build the alert object
        """
        groupSettings = self.dmd.ZenUsers.getGroupSettings(alertGroup)
        ids = []
        for alert in groupSettings.getActionRules():
            ids.append(alert.id)
        if alertName not in ids:
            groupSettings.manage_addActionRule(alertName)
            for alert in groupSettings.getActionRules():
                if alert.id == alertName:
                    alert.enabled = self.enabled
                    alert.where = alertWhere
                    alert.clearFormat = alert.clearFormat.replace('[zenoss]',alertName)
                    alert.format = alert.format.replace('[zenoss]',alertName)

    def buildAlertName(self,usergroup):
        """ create standardized alert name
        """
        if usergroup == self.module.getRelatedId():
            alertName = self.module.getRelatedId() + '-' + self.id 
        else:
            alertName = usergroup + '-' + self.module.getRelatedId() + '-' + self.id 
        return alertName
    
    def buildAlertWhere(self):
        """ build filters for alert definition
        """
        condition = 'severity >= 3 and eventState = 0 and prodState = 1000'
        for sys in self.module.moduleSystemOrganizers:
            condition += ' and (systems like \'%|' + sys + '%\')'
        for grp in self.module.moduleGroupOrganizers:
            condition += ' and (deviceGroups like \'%|' + grp + '%\')'
        if self.propertyType == 'Osprocess':
            condition += ' and (eventClass like \'/Status/OSProcess%\')'
            condition += ' and (component like \'%' + self.propertyName + '%\')'
        if self.propertyType == 'Ipservice':
            condition += ' and (eventClass like \'/Status/IpService%\')'
            condition += ' and (component like \'%' + self.propertyName + '%\')'
        if self.propertyType == 'Winservice':
            condition += ' and (eventClass like \'/Status/WinService%\')'
            condition += ' and (component like \'%' + self.propertyName + '%\')'
        return condition
    
    def findTemplateProperties(self):
        for template in self.dmd.Devices.getAllRRDTemplates():
            if template.id.find(self.propertyName) >=0:
                # find all data sources
                for ds in template.getRRDDataSources():
                    eventclass = ds.eventClass
                    
                return True
    
    def manage_buildRuleAlert(self, REQUEST=None):
        """ build alerts from menu
        """
        alert = self.createRuleAlert()
        if REQUEST:
            if alert:
                messaging.IMessageSender(self).sendToBrowser(
                    'Alert Built',
                    'Alert built: %s' % self.id
                )
            return self.callZenScreen(REQUEST)
        
    def getRuleGroupSettings(self):
        """ get the dmd Groups objects and properties
        """
        groupSettings = []
        for m in self.module.moduleGroupOrganizers:
            settings = self.dmd.Groups.getOrganizer(m)
            groupSettings.append(settings)
        return groupSettings
    
    def getRuleSystemSettings(self):
        """ get the dmd Systems objects and properties
        """
        groupSettings = []
        for m in self.module.moduleSystemOrganizers:
            settings = self.dmd.Systems.getOrganizer(m)
            groupSettings.append(settings)
        return groupSettings
    
    

