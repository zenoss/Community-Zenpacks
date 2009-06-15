__doc__="""AIX Cdrom

"""
__version__ = "$Revision: 1.7 $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *

from Products.ZenModel.HWComponent import HWComponent

from Products.ZenModel.ZenossSecurity import *

def manage_addCdrom(context, id, title = None, REQUEST = None):
    """make a filesystem"""
    cd = AIXCdrom(id, title)
    context._setObject(id, cd)
    cd = context._getOb(id)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main')

addCdrom = DTMLFile('dtml/addCdrom',globals())


class AIXCdrom(HWComponent):
    """AIX CDrom object"""

    portal_type = meta_type = 'Cdrom'

    manage_editCdromForm = DTMLFile('dtml/manageEditCdrom',globals())

    description = ""
    hostresindex = 0

    title=""
    aixcdromtype=""
    aixcdrominterface=""
    aixcdromdescription=""
    aixcdromstatus=""
    aixcdromlocation=""
    aixcdromManufacturerName=""
    aixcdromModelName=""
    aixcdromPartNumber=""
    aixcdromFRU=""
    aixcdromEC=""



    _properties = HWComponent._properties + (
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'hostresindex', 'type':'int', 'mode':'w'},
                 {'id':'title', 'type':'string', 'mode':'w'},
                 {'id':'aixcdromtype', 'type':'string', 'mode':'w'},
                 {'id':'aixcdrominterface', 'type':'string', 'mode':'w'},
                 {'id':'aixcdromdescription', 'type':'string', 'mode':'w'},
                 {'id':'aixcdromstatus', 'type':'string', 'mode':'w'},
                 {'id':'aixcdromlocation', 'type':'string', 'mode':'w'},
                 {'id':'aixcdromManufacturerName', 'type':'string', 'mode':'w'},
                 {'id':'aixcdromModelName', 'type':'string', 'mode':'w'},
                 {'id':'aixcdromPartNumber', 'type':'string', 'mode':'w'},
                 {'id':'aixcdromFRU', 'type':'string', 'mode':'w'},
                 {'id':'aixcdromEC', 'type':'string', 'mode':'w'},
                )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXDeviceHW", "cdrom")),
        )


    factory_type_information = (
        {
            'id'             : 'Cdrom',
            'meta_type'      : 'Cdrom',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCdrom',
            'immediate_view' : 'viewCdrom',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCdrom'
                , 'permissions'   : ('View',)
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

    def viewName(self): return self.description


InitializeClass(AIXCdrom)
