__doc__="""AIX Tape

"""
__version__ = "$Revision: 1.7 $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *

from Products.ZenModel.HWComponent import HWComponent

from Products.ZenModel.ZenossSecurity import *

def manage_addtape(context, id, title = None, REQUEST = None):
    """make a filesystem"""
    tape = AIXTape(id, title)
    context._setObject(id, tape)
    tape = context._getOb(id)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main')

addtape = DTMLFile('dtml/addtape',globals())


class AIXTape(HWComponent):
    """AIX tape object"""

    portal_type = meta_type = 'Tape'

    manage_edittapedriveForm = DTMLFile('dtml/manageEdittape',globals())

    description = ""
    hostresindex = 0

    title = ""
    aixtapedrivetype = ""
    aixtapedriveinterface = ""
    aixtapedrivestatus = ""
    aixtapedrivedescription = ""
    aixtapedrivelocation = ""
    aixtapedriveblksize = ""
    aixtapedriveManufacturerName = ""
    aixtapedriveModelName = ""
    aixtapedriveSerialNumber = ""
    aixtapedrivePartNumber = ""
    aixtapedriveFRU = ""
    aixtapedriveEC = ""


    _properties = HWComponent._properties + (
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'hostresindex', 'type':'int', 'mode':'w'},
                 {'id':'title', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedrivetype', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedriveinterface', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedrivestatus', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedrivedescription', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedrivelocation', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedriveblksize', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedriveManufacturerName', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedriveModelName', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedriveSerialNumber', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedrivePartNumber', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedriveFRU', 'type':'string', 'mode':'w'},
                 {'id':'aixtapedriveEC', 'type':'string', 'mode':'w'},
                )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXDeviceHW", "tape")),
        )


    factory_type_information = (
        {
            'id'             : 'Tape',
            'meta_type'      : 'Tape',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addtape',
            'immediate_view' : 'viewtape',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewtape'
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


InitializeClass(AIXTape)
