from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.OSComponent import OSComponent
import copy

class AIXPrintQueue(OSComponent):
    "Aix PrintQueue class"

    # Set so a template named PrintQueue will bind automatically
    portal_type = meta_type = 'PrintQueue'

    # Attribute Defaults
    aixprintqueuename = ""
    aixprintqueuedevice = ""
    aixprintqueuestate = ""
    aixprintqueueaction = ""
    aixprintqueuedescipline = ""
    aixprintqueueacctfile = ""
    aixprintqueuehost = ""
    aixprintqueueRQ = ""
    aixprintqueueJobNum = ""

    # Define New Properties for this class
    _properties = OSComponent._properties + (
        {'id':'aixprintqueuename', 'type':'string', 'mode':''},
        {'id':'aixprintqueuedevice', 'type':'string', 'mode':''},
        {'id':'aixprintqueuestate', 'type':'string', 'mode':''},
        {'id':'aixprintqueueaction', 'type':'string', 'mode':''},
        {'id':'aixprintqueuedescipline', 'type':'string', 'mode':''},
        {'id':'aixprintqueueacctfile', 'type':'string', 'mode':''},
        {'id':'aixprintqueuehost', 'type':'string', 'mode':''},
        {'id':'aixprintqueueRQ', 'type':'string', 'mode':''},
        {'id':'aixprintqueueJobNum', 'type':'string', 'mode':''},
    )

    # Define new relationships
    _relations =(
        ("os", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXOperatingSystem", "printqueue")),
        )

    # Define tabs and screen templates to use when this component is selected
    factory_type_information = (
        {
            'id'             : 'PrintQueue',
            'meta_type'      : 'PrintQueue',
            'description'    : """print queue grouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addPrintQueue',
            'immediate_view' : 'viewPrintQueue',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewPrintQueue'
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

    def viewName(self):
        return self.id

    name = primarySortKey = viewName


 
    def stateString(self):
        """
        Return the state stored in the rrd file
        Used for print queue state string ... does not define status
        Status defined via thresholds
        """
        statemap = ['Ready', 'Running', 'Waiting', 'Offline', 'Operator Message Wait',
                     'Init', 'Sending', 'GetHost', 'Connect', 'Busy']


        # Datapoint defined in the template	
        state = self.getRRDValue('aixprintqueueStatus_aixprintqueueStatus')
        if state == None:
            if self.aixprintqueuestate == "":
                return "Unknown"
            return statemap[int(self.aixprintqueuestate)-1]
        return statemap[int(state)-1]

InitializeClass(AIXPrintQueue)
