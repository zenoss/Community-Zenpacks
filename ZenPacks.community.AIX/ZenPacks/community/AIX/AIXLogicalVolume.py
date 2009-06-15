from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from Products.ZenRelations.RelSchema import *
from Products.ZenUtils.Utils import prepId
from Products.ZenWidgets import messaging
from Products.ZenModel.Service import Service
from Products.ZenModel.OSProcess import OSProcess
from Products.ZenModel.OSComponent import OSComponent
from ZenPacks.community.AIX.AIXFileSystem import manage_addFileSystem
from ZenPacks.community.AIX.AIXPaging import manage_addPaging
from Globals import DTMLFile
import copy
import types

import logging
log = logging.getLogger("zen.AIXLogicalVolume")


def manage_addLogicalVolume(context, id, userCreated, REQUEST=None):
    """make a logicalvolume"""
    lvid = prepId(id)
    lv = AIXLogicalVolume(lvid)
    context._setObject(lvid, lv)
    lv = context._getOb(lvid)
    if userCreated: lv.setUserCreateFlag()
    if REQUEST is not None:
       REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return lv

addLogicalVolume = DTMLFile('dtml/addLogicalVolume',globals())


class AIXLogicalVolume(OSComponent):
    "Aix Logical Volumes class"

    # Set so a template named PrintQueue will bind automatically
    portal_type = meta_type = 'LogicalVolume'

    # Attribute Defaults
    title = ""
    aixLvNameVg = ""
    aixLvType = ""
    aixLvMountPoint = ""
    aixLvSize = ""
    aixLvState = ""

    # Define New Properties for this class
    _properties = OSComponent._properties + (
        {'id':'title', 'type':'string', 'mode':''},
        {'id':'aixLvNameVg', 'type':'string', 'mode':''},
        {'id':'aixLvType', 'type':'string', 'mode':''},
        {'id':'aixLvMountPoint', 'type':'string', 'mode':''},
        {'id':'aixLvSize', 'type':'string', 'mode':''},
        {'id':'aixLvState', 'type':'string', 'mode':''},
    )

    # Define new relationships
    _relations = (
        ('volumegroup', ToOne(ToManyCont, 'ZenPacks.community.AIX.AIXVolumeGroup', 'logicalvolume')),
        ('filesystem', ToManyCont(ToOne, 'ZenPacks.community.AIX.AIXFileSystem', 'logicalvolume')),
        ('paging', ToManyCont(ToOne, 'ZenPacks.community.AIX.AIXPaging', 'logicalvolume')),
    )

    # Define tabs and screen templates to use when this component is selected
    factory_type_information = (
        {
            'id'             : 'LogicalVolume',
            'meta_type'      : 'LogicalVolume',
            'description'    : """logical volume grouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addLogicalVolume',
            'immediate_view' : 'viewLogicalVolume',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewLogicalVolume'
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

    def getFsSetup(self, fs_data):
        # Create a new filesystem object
        fs=manage_addFileSystem(self.filesystem, fs_data['mount'], False)
        for key in fs_data.keys():
            fs_attr = getattr( fs, key)
            setattr(fs, key, fs_data[key])

    def getPagingSetup(self, paging_data):
        # Create a new paging object
        paging=manage_addPaging(self.paging, paging_data['aixPageName'], False)
        for key in paging_data.keys():
            paging_attr = getattr(paging, key, None)
            setattr(paging, key, paging_data[key])

    # Function used to return the fs objects for the web interface
    def getfsobjs(self):
        """Takes no arguments but returns a set of fs objects """
        return self.filesystem.objectValuesAll()

    def setFSMonitored(self, componentNames=[],
                               monitored=True, REQUEST=None):
        """
        Set monitored status for selected components.
        """
        comp_mount_names = []
        if not componentNames: return self()
        if isinstance(componentNames, basestring):
            componentNames = (componentNames,)
        monitored = bool(monitored)
        for componentName in componentNames:
            for obj in self.getfsobjs():
                if obj.id == componentName:
                    comp = obj
                    comp_mount_names.append(comp.mount)
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
                                              ', '.join(comp_mount_names))
            )
            return self.callZenScreen(REQUEST)

    def unlockFSComponents(self, componentNames=[], REQUEST=None):
        """Unlock device components"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.getfsobjs():
                if obj.id == componentName:
                    obj.unlock()
        if REQUEST:
            return self.callZenScreen(REQUEST)

    def lockFSComponentsFromDeletion(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock device components from deletion"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.getfsobjs():
                if obj.id == componentName:
                    obj.lockFromDeletion(sendEventWhenBlocked)
        if REQUEST:
            return self.callZenScreen(REQUEST)

    def lockFSComponentsFromUpdates(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock device components from updates"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.getfsobjs():
                if obj.id == componentName:
                    obj.lockFromUpdates(sendEventWhenBlocked)
        if REQUEST:
            return self.callZenScreen(REQUEST)

    def unlockFileSystems(self, componentNames=[], REQUEST=None):
        """Unlock FileSystems"""
        self.unlockFSComponents(componentNames, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Filesystems Unlocked',
                'Filesystems %s were unlocked.' % (', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    def lockFileSystemsFromDeletion(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock FileSystems from deletion"""
        self.lockFSComponentsFromDeletion(componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Filesystems Locked',
                'Filesystems %s were locked from deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    def lockFileSystemsFromUpdates(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock FileSystems from updates"""
        self.lockFSComponentsFromUpdates(componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Filesystems Locked',
                'Filesystems %s were locked from updates and deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

InitializeClass(AIXLogicalVolume)
