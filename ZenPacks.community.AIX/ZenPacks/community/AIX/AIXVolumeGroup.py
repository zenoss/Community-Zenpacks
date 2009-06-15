import logging
log = logging.getLogger("zen.AIXVolumeGroup")

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.OSComponent import OSComponent
from Products.ZenModel.Service import Service
from Products.ZenModel.OSProcess import OSProcess
from Products.ZenWidgets import messaging
from ZenPacks.community.AIX.AIXLogicalVolume import manage_addLogicalVolume
from ZenPacks.community.AIX.AIXPhysicalVolume import manage_addPhysicalVolume
import copy
import types

class AIXVolumeGroup(OSComponent):
    "Aix Volume Group class"

    # Set so a template named PrintQueue will bind automatically
    portal_type = meta_type = 'VolumeGroup'

    # Attribute Defaults
    title = ""
    aixVgIdentifier = ""
    aixVgState = ""
    aixVgSize = ""
    aixVgFree = ""
    aixVgCurNumLVs = ""
    aixVgOpenLVs = ""
    aixVgActiveLVs = ""

    # Define New Properties for this class
    _properties = OSComponent._properties + (
        {'id':'title', 'type':'string', 'mode':''},
        {'id':'aixVgIdentifier', 'type':'string', 'mode':''},
        {'id':'aixVgState', 'type':'string', 'mode':''},
        {'id':'aixVgSize', 'type':'string', 'mode':''},
        {'id':'aixVgFree', 'type':'string', 'mode':''},
        {'id':'aixVgCurNumLVs', 'type':'string', 'mode':''},
        {'id':'aixVgOpenLVs', 'type':'string', 'mode':''},
        {'id':'aixVgActiveLVs', 'type':'string', 'mode':''},
    )

    # Define new relationships
    _relations =(
        ("os", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXOperatingSystem","volumegroup")),
        ('logicalvolume', ToManyCont(ToOne, 'ZenPacks.community.AIX.AIXLogicalVolume', 'volumegroup')),
        ('physicalvolume', ToManyCont(ToOne, 'ZenPacks.community.AIX.AIXPhysicalVolume', 'volumegroup')),
        )

    # Define tabs and screen templates to use when this component is selected
    factory_type_information = (
        {
            'id'             : 'VolumeGroup',
            'meta_type'      : 'VolumeGroup',
            'description'    : """volume groupgrouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addVolumeGroup',
            'immediate_view' : 'viewVolumeGroup',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewVolumeGroup'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : ("Change Device", )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

    def getLvSetup(self, lv_data):
        # Do work to extract the information ...
        for key in lv_data.keys():
            lv=manage_addLogicalVolume(self.logicalvolume, key, False)
            for subkey in lv_data[key]:
                log.debug("LV Subkey %s -> data %s" %( subkey, lv_data[key][subkey]))
                lv_attr = getattr( lv, subkey)
                if callable( lv_attr ):
                    lv_attr(lv_data[key][subkey])
                else:
                    setattr(lv, subkey, lv_data[key][subkey])

    def getPvSetup(self, pv_data):
        # Do work to extract the information ...
        for key in pv_data.keys():
            pv=manage_addPhysicalVolume(self.physicalvolume, key, False)
            for subkey in pv_data[key]:
                log.debug("PV Subkey %s -> data %s" %( subkey, pv_data[key][subkey]))
                pv_attr = getattr( pv, subkey)
                if callable( pv_attr ):
                    pv_attr(pv_data[key][subkey])
                else:
                    setattr(pv, subkey, pv_data[key][subkey])

    def setLVMonitored(self, componentNames=[],
                               monitored=True, REQUEST=None):
        """
        Set monitored status for selected components.
        """
        comp_ids = []
        if not componentNames: return self()
        if isinstance(componentNames, basestring):
            componentNames = (componentNames,)
        monitored = bool(monitored)
        for componentName in componentNames:
            for obj in self.logicalvolume.objectValuesAll():
                if obj.id == componentName:
                    comp = obj
                    comp_ids.append(comp.id)
            if comp and comp.monitored() != monitored:
                comp.monitor = monitored
                if isinstance(comp, (Service, OSProcess)):
                    comp.setAqProperty('zMonitor', monitored, 'boolean')
                comp.index_object()
        if REQUEST:
            verb = monitored and "Enabled" or "Disabled"
            messaging.IMessageSender(self).sendToBrowser(
                'Monitoring %s' % verb,
                'Monitoring was %s on %s.' % (verb.lower(),
                                              ', '.join(comp_ids))
            )
            return self.callZenScreen(REQUEST)

    def setPVMonitored(self, componentNames=[],
                               monitored=True, REQUEST=None):
        """
        Set monitored status for selected components.
        """
        comp_ids = []
        if not componentNames: return self()
        if isinstance(componentNames, basestring):
            componentNames = (componentNames,)
        monitored = bool(monitored)
        for componentName in componentNames:
            for obj in self.physicalvolume.objectValuesAll():
                if obj.id == componentName:
                    comp = obj
                    comp_ids.append(comp.id)
            if comp and comp.monitored() != monitored:
                comp.monitor = monitored
                if isinstance(comp, (Service, OSProcess)):
                    comp.setAqProperty('zMonitor', monitored, 'boolean')
                comp.index_object()
        if REQUEST:
            verb = monitored and "Enabled" or "Disabled"
            messaging.IMessageSender(self).sendToBrowser(
                'Monitoring %s' % verb,
                'Monitoring was %s on %s.' % (verb.lower(),
                                              ', '.join(comp_ids))
            )
            return self.callZenScreen(REQUEST)

    # New
    def unlockLVComponents(self, componentNames=[], REQUEST=None):
        """Unlock device components"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.logicalvolume.objectValuesAll():
                if obj.id == componentName:
                    obj.unlock()
        if REQUEST:
            return self.callZenScreen(REQUEST)


    # New
    def lockLVComponentsFromUpdates(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock device components from updates"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.logicalvolume.objectValuesAll():
                if obj.id == componentName:
                    obj.lockFromUpdates(sendEventWhenBlocked)
        if REQUEST:
            return self.callZenScreen(REQUEST)

    # New
    def unlockLogicalVolumes(self, componentNames=[], REQUEST=None):
        """Unlock Logical Volumes"""
        self.unlockLVComponents(componentNames, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Logical Volumes Unlocked',
                'Logical Volumes %s were unlocked.' % (', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    # New
    def lockLogicalVolumesFromDeletion(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock Logical Volumes from deletion"""
        self.lockLVComponentsFromDeletion(componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Logical Volumes Locked',
                'Logical Volumes %s were locked from deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    # New
    def lockLogicalVolumesFromUpdates(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock Logical Volumes from updates"""
        self.lockLVComponentsFromUpdates(componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Logical Volumes Locked',
                'Logical Volumes %s were locked from updates and deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    # New
    def lockPVComponentsFromUpdates(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock device components from updates"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.physicalvolume.objectValuesAll():
                if obj.id == componentName:
                    obj.lockFromUpdates(sendEventWhenBlocked)
        if REQUEST:
            return self.callZenScreen(REQUEST)

    # New
    def unlockPVComponents(self, componentNames=[], REQUEST=None):
        """Unlock device components"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.physicalvolume.objectValuesAll():
                if obj.id == componentName:
                    obj.unlock()
        if REQUEST:
            return self.callZenScreen(REQUEST)
    # New
    def unlockPhysicalVolumes(self, componentNames=[], REQUEST=None):
        """Unlock Physical Volumes"""
        self.unlockPVComponents(componentNames, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Physical Volumes Unlocked',
                'Physical Volumes %s were unlocked.' % (', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    # New
    def lockPhysicalVolumesFromDeletion(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock Physical Volumes from deletion"""
        self.lockPVComponentsFromDeletion(componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Physical Volumes Locked',
                'Physical Volumes %s were locked from deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    # New
    def lockPhysicalVolumesFromUpdates(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock Physical Volumes from updates"""
        self.lockPVComponentsFromUpdates(componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Physical Volumes Locked',
                'Physical Volumes %s were locked from updates and deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

InitializeClass(AIXVolumeGroup)
