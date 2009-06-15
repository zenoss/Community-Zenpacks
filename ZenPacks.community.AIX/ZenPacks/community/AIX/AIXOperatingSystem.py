import types
from Globals import InitializeClass
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.Software import Software
from Products.ZenRelations.RelSchema import *
from Products.ZenWidgets import messaging
from Products.ZenModel.Service import Service
from Products.ZenModel.OSProcess import OSProcess

import logging
log = logging.getLogger("zen.AIXOperatingSystem")

class AIXOperatingSystem(OperatingSystem):

    factory_type_information = (
        {
            'id'             : 'Device',
            'meta_type'      : 'Device',
            'description'    : """Base class for all devices""",
            'icon'           : 'Device_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addDevice',
            'immediate_view' : '../aixdeviceOsDetail',
            'actions'        : ()
         },
        )

    # Redefine relationships for aix

    _relations = Software._relations + (
        ("interfaces", ToManyCont(ToOne,
            "Products.ZenModel.IpInterface", "os")),
        ("routes", ToManyCont(ToOne, "Products.ZenModel.IpRouteEntry", "os")),
        ("ipservices", ToManyCont(ToOne, "Products.ZenModel.IpService", "os")),
        ("winservices", ToManyCont(ToOne,
            "Products.ZenModel.WinService", "os")),
        ("processes", ToManyCont(ToOne, "Products.ZenModel.OSProcess", "os")),
        ("software", ToManyCont(ToOne, "Products.ZenModel.Software", "os")),
        ('printqueue', ToManyCont(ToOne, 'ZenPacks.community.AIX.AIXPrintQueue', 'os')),
        ('volumegroup', ToManyCont(ToOne, 'ZenPacks.community.AIX.AIXVolumeGroup', 'os')),
    )

    # Functions listed below are overridden or are new

    # Function used to return the vg objects for the web interface
    # New
    def getvgobjs(self):
        """Takes no arguments but returns a set of vg objects """
        vgobjs = []
        vgobjs = self.volumegroup.objectValuesAll()
        return vgobjs

    # Function used to return the lv objects for the web interface
    # New
    def getlvobjs(self):
        """Takes no arguments but returns a set of lv objects """
        lvobjs = []
        vgobjs = self.getvgobjs()
        for obj in vgobjs:
            lvobjs = lvobjs + obj.logicalvolume.objectValuesAll()
        return lvobjs

    # Function used to return the fs objects for the web interface
    # New
    def getfsobjs(self):
        """Takes no arguments but returns a set of fs objects """
        fsobjs = []
        lvobjs = self.getlvobjs()
        for obj in lvobjs:
            fsobjs = fsobjs + obj.filesystem.objectValuesAll()
        return fsobjs

    # Overridden
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

    # New
    def setVGMonitored(self, componentNames=[],
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
            for obj in self.getvgobjs():
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

    # Overridden
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

    # Overridden
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

    # Overridden
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

    # Overridden
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

    # Overridden
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

    # Overridden
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

    # New
    def unlockVGComponents(self, componentNames=[], REQUEST=None):
        """Unlock device components"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.getvgobjs():
                if obj.id == componentName:
                    obj.unlock()
        if REQUEST:
            return self.callZenScreen(REQUEST)

    # New
    def lockFSComponentsFromDeletion(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock device components from deletion"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.getvgobjs():
                if obj.id == componentName:
                    obj.lockFromDeletion(sendEventWhenBlocked)
        if REQUEST:
            return self.callZenScreen(REQUEST)

    # New
    def lockVGComponentsFromUpdates(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock device components from updates"""
        if not componentNames: return self()
        if type(componentNames) in types.StringTypes:
            componentNames = (componentNames,)
        for componentName in componentNames:
            for obj in self.getvgobjs():
                if obj.id == componentName:
                    obj.lockFromUpdates(sendEventWhenBlocked)
        if REQUEST:
            return self.callZenScreen(REQUEST)

    # New
    def unlockVolumeGroups(self, componentNames=[], REQUEST=None):
        """Unlock Volume Groups"""
        self.unlockVGComponents(componentNames, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Volume Groups Unlocked',
                'Volume Groups %s were unlocked.' % (', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    # New
    def lockVolumeGroupsFromDeletion(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock Volume Groups from deletion"""
        self.lockVGComponentsFromDeletion(componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Volume Groups Locked',
                'Volume Groupss %s were locked from deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    # New
    def lockVolumeGroupsFromUpdates(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock Volume Groups from updates"""
        self.lockVGComponentsFromUpdates(componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Volume Groups Locked',
                'Volume Groups %s were locked from updates and deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    # New
    def setPQMonitored(self, componentNames=[],
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
            for obj in self.printqueue.objectValuesAll():
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
    def unlockPrintQueues(self, componentNames=[], REQUEST=None):
        """Unlock Print Queues"""
        self.unlockDeviceComponents(self.printqueue,componentNames, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Print Queues Unlocked',
                'Print Queues %s were unlocked.' % (', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    #New
    def lockPrintQueuesFromDeletion(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock Print Queues from deletion"""
        self.lockDeviceComponentsFromDeletion(self.printqueue,componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Print Queues Locked',
                'Print Queues %s were locked from deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

    #New
    def lockPrintQueuesFromUpdates(self, componentNames=[],
            sendEventWhenBlocked=None, REQUEST=None):
        """Lock Print Queues from updates"""
        self.lockDeviceComponentsFromUpdates(self.printqueue,componentNames,
            sendEventWhenBlocked, REQUEST)
        if REQUEST:
            messaging.IMessageSender(self).sendToBrowser(
                'Print Queues Locked',
                'Print Queues %s were locked from updates and deletion.' % (
                    ', '.join(componentNames))
            )
            REQUEST['RESPONSE'].redirect(self.absolute_url())
            return self.callZenScreen(REQUEST)

InitializeClass(AIXOperatingSystem)
