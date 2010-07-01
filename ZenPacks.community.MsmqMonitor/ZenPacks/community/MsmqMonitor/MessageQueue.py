
import rrdtool
from Globals import DTMLFile
from Globals import InitializeClass

from ZenPacks.community.deviceAdvDetail.HWStatus import *

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenRelations.RelSchema import *
from Products.ZenUtils.Utils import prepId, zenPath
from Products.ZenRRD.RRDUtil import RRDUtil
from Products.ZenModel.OSComponent import OSComponent

from Products.ZenModel.ZenossSecurity import *

def manage_addMessageQueue(context, id, queueType, userCreated, REQUEST=None):
    """
    Create a Message Queue.
    """
    mqid = prepId(id)
    mq = MessageQueue(mqid)
    context._setObject(mqid, mq)
    mq = context._getOb(mqid)
    if type: mq.setType(queueType)
    if userCreated: mq.setUserCreateFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')

addMessageQueue = DTMLFile('dtml/addMessageQueue',globals())

class MessageQueue(OSComponent, HWStatus):
    """
    MessageQueue. Subclasses OSComponent and HWStatus.
    """

    ZENPACKID = 'ZenPacks.community.MsmqMonitor'

    portal_type = meta_type = 'MessageQueue'

    manage_editMessageQueueForm = DTMLFile('dtml/editMessageQueue',globals())

    queueType = ''
    queueCount = 0
    queueStatus = 1

    statusMap = {1: (DOT_GREY,  SEV_WARNING, 'Unknown'),
                 2: (DOT_GREEN, SEV_CLEAN,   'Active'),
                 3: (DOT_ORANGE,SEV_WARNING, 'Warning'),
                 4: (DOT_RED,   SEV_CRITICAL,'Critical'),
                }

    _properties = OSComponent._properties + (
        {'id':'queueType','type':'string','mode':'w'},
        {'id':'queueCount','type':'int','mode':'w'},
        {'id':'queueStatus','type':'int','mode':'w'},
        )

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont, "Products.ZenModel.OperatingSystem","msmq")),
        )

    factory_type_information = (
        {
            'id'            : 'MessageQueue',
            'meta_type'     : 'MessageQueue',
            'description'   : """Message Queue (MSMQ)""",
            'product'       : 'MsmqMonitor',
            'factory'       : 'manage_addMessageQueue',
            'immediate_view': 'viewMessageQueue',
            'actions'       : (
                { 'id'          : 'status'
                 ,'name'        : 'Status'
                 ,'action'      : 'viewMessageQueue'
                 ,'permissions' : (ZEN_VIEW,)
                },
                { 'id'          : 'events'
                 ,'name'        : 'Events'
                 ,'action'      : 'viewEvents'
                 ,'permissions' : (ZEN_VIEW,)
                },
                { 'id'          : 'perfConf'
                 ,'name'        : 'Template'
                 ,'action'      : 'objTemplates'
                 ,'permissions' : ("Change Device",)
                },
                { 'id'          : 'viewHistory'
                 ,'name'        : 'Modifications'
                 ,'action'      : 'viewHistory'
                 ,'permissions' : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
        },
        )

    def getCount(self):
        """
        Retrieve current count from RRD.
        """
        filename = self.getRRDFileName('queueCount_queueCount')
        try:
            count = rrdtool.info(zenPath('perf') + '/'
                + filename)['ds[ds0].last_ds']
        except:
            count = '0'
        if '.' in count:
            count, discard = count.split('.',1)
        return count

    def getRRDNames(self):
        """
        Return the name of the RRD data source.
        """
        return ['queueCount_queueCount']

    def viewName(self):
        """
        Accessor method to retrieve the queue name.
        """
        return self.id

    def viewType(self):
        """
        Accessor method to retrieve the queue type.
        """
        return self.queueType

    def setType(self, queueType):
        """
        Setter method to change the queue type.
        """
        self.queueType = queueType
        return self.queueType

    def viewCount(self):
        """
        Accessor method to retrieve the queue count as a string.
        """
        return "%s" % self.getCount()

    def manage_editMessageQueue(self, monitor=False, queueType=None, REQUEST=None):
        """
        Callback function used when editing the Message Queue from the WebUI
        """
        if queueType:
            self.queueType = queueType

        self.monitor = monitor
        self.index_object()

        if REQUEST:
            REQUEST['message'] = "Queue updated."
            return self.callZenScreen(REQUEST)

InitializeClass(MessageQueue)

