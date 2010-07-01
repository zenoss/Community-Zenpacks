
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenUtils.Utils import prepId
from Products.ZenWidgets import messaging
from MessageQueue import manage_addMessageQueue

def addMessageQueue(self, id, queueType, userCreated, REQUEST=None):
    """
    Callback function assigned to the OS object to act as the direct callback
    for the "addMessageQueue" dialog.
    """
    mqid = prepId(id)
    manage_addMessageQueue(self.msmq, id, queueType, userCreated)
    self._p_changed = True
    if REQUEST is not None:
        messaging.IMessageSender(self).sendToBrowser(
                'Queue Created',
                'Message Queue %s was created.' % id
                )
        REQUEST['RESPONSE'].redirect(
                self.msmq._getOb(mqid).absolute_url())
        return self.callZenScreen(REQUEST)

def deleteMessageQueues(self, componentNames=[], REQUEST=None):
    """
    Callback function assigned to the OS object to act as the direct callback
    for the "deleteMessageQueues" dialog.
    """
    self.deleteDeviceComponents(self.msmq, componentNames, REQUEST)
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
                'Queues Deleted',
                'Message Queues %s were deleted.' % (
                    ', '.join(componentNames))
                )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

def setComponentMonitored(self, context, componentNames=[],
                          monitored=True, REQUEST=None):
    """
    Callback function assigned to the OS object to act as the direct callback
    for the "changeMonitoring" dialog.
    """
    if isinstance(context, basestring):
        context = getattr(self, context)
    if not componentNames: return self()
    if isinstance(componentNames, basestring):
        componentNames = (componentNames,)
    monitored = bool(monitored)
    for componentName in componentNames:
        comp = context._getOb(componentName, False)
        if comp and comp.monitored() != monitored:
            comp.monitor = monitored
            comp.index_object()
    if REQUEST:
        verb = monitored and "Enabled" or "Disabled"
        messaging.IMessageSender(self).sendToBrowser(
                'Monitoring %s' % verb,
                'Monitoring was %s on %s.' % (verb.lower(),
                                              ', '.join(componentNames))
                )
        return self.callZenScreen(REQUEST)

def unlockMessageQueues(self, componentNames=[], REQUEST=None):
    """
    Callback function that unlocks queues.
    """
    self.unlockDeviceComponents(self.msmq, componentNames, REQUEST)
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Queues Unlocked',
            'Message Queues %s were unlocked.' % (', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)

def lockMessageQueuesFromDeletion(self, componentNames=[], sendEventWhenBlocked=None, REQUEST=None):
    """
    Callback function that prevents queues from being deleted by the modeler.
    """
    self.lockDeviceComponentsFromDeletion(self.msmq, componentNames, sendEventWhenBlocked, REQUEST)
    self.lockDeviceComponentsFromUpdates(self.msmq, componentNames, sendEventWhenBlocked, REQUEST)
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Queues Locked',
            'Message Queues %s were locked from deletion.' % (', '.join(componentNames))
        )
        REQUEST['RESPONSE'].redirect(self.absolute_url())
        return self.callZenScreen(REQUEST)


from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenRelations.RelSchema import *
OperatingSystem._relations += (("msmq", ToManyCont(ToOne,"ZenPacks.community.MsmqMonitor.MessageQueue","os")), )
OperatingSystem.addMessageQueue = addMessageQueue
OperatingSystem.deleteMessageQueues = deleteMessageQueues
OperatingSystem.setComponentMonitored = setComponentMonitored
OperatingSystem.lockMessageQueuesFromDeletion = lockMessageQueuesFromDeletion
OperatingSystem.unlockMessageQueues = unlockMessageQueues

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
class ZenPack(ZenPackBase):
    """
    This class extends the ZenPack methods to perform specific pre/post install,
    upgrade or uninstall steps.
    """

    def install(self, app):
        """
        Create the top-level menu.
        """
        if hasattr(self.dmd.zenMenus, 'MessageQueues'):
            self.dmd.zenMenus._delObject('MessageQueues')
        self.dmd.zenMenus.manage_addZenMenu('MessageQueues')
        ZenPackBase.install(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

    def upgrade(self, app):
        """
        Delete and re-create the top-level menu.
        """
        if hasattr(self.dmd.zenMenus, 'MessageQueues'):
            self.dmd.zenMenus._delObject('MessageQueues')
        self.dmd.zenMenus.manage_addZenMenu('MessageQueues')
        ZenPackBase.upgrade(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

    def remove(self, app, junk):
        """
        Delete the top-level menu.
        """
        ZenPackBase.remove(self, app, junk)
        if hasattr(self.dmd.zenMenus, 'MessageQueues'):
            self.dmd.zenMenus._delObject('MessageQueues')
        OperatingSystem._relations = tuple([x for x in
                                            OperatingSystem._relations if x[0]
                                            != 'msmq'])
        for d in self.dmd.Devices.getSubDevices():
            d.os.buildRelations()

