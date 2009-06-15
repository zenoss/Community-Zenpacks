__doc__="""AIX Printer

"""
__version__ = "$Revision: 1.7 $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *

from Products.ZenModel.HWComponent import HWComponent

from Products.ZenModel.ZenossSecurity import *

def manage_addPrinter(context, id, title = None, REQUEST = None):
    """make a printer"""
    pr = AIXPrinter(id, title)
    context._setObject(id, pr)
    pr = context._getOb(id)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main')

addPrinter = DTMLFile('dtml/addPrinter',globals())


class AIXPrinter(HWComponent):
    """AIX Printer object"""

    portal_type = meta_type = 'Printer'

    manage_editPrinterForm = DTMLFile('dtml/manageEditPrinter',globals())

    description = ""
    hostresindex = 0

    title = ""
    aixprintertype = ""
    aixprinterinterface = ""
    aixprinterstatus = ""
    aixprinterdescription = ""
    aixprinterlocation = ""
    aixprinterportnumber = ""

    _properties = HWComponent._properties + (
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'hostresindex', 'type':'int', 'mode':'w'},
                 {'id':'title', 'type':'string', 'mode':'w'},
                 {'id':'aixprintertype', 'type':'string', 'mode':'w'},
                 {'id':'aixprinterinterface', 'type':'string', 'mode':'w'},
                 {'id':'aixprinterstatus', 'type':'string', 'mode':'w'},
                 {'id':'aixprinterdescription', 'type':'string', 'mode':'w'},
                 {'id':'aixprinterlocation', 'type':'string', 'mode':'w'},
                 {'id':'aixprinterportnumber', 'type':'string', 'mode':'w'},
                )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXDeviceHW", "printer")),
        )


    factory_type_information = (
        {
            'id'             : 'Printer',
            'meta_type'      : 'Printer',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addPrinter',
            'immediate_view' : 'viewPrinter',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewPrinter'
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


InitializeClass(AIXPrinter)
