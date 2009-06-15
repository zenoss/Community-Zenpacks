__doc__="""AIX Lpar Info

"""
__version__ = "$Revision: 1.7 $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *

from Products.ZenModel.HWComponent import HWComponent

from Products.ZenModel.ZenossSecurity import *

def manage_addLparInfo(context, id, title = None, REQUEST = None):
    """make a lparinfo object"""
    lp = AIXLparInfo(id, title)
    context._setObject(id, lp)
    lp = context._getOb(id)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main')

addLparInfo = DTMLFile('dtml/addLparInfo',globals())


class AIXLparInfo(HWComponent):
    """AIX LparInfo object"""

    portal_type = meta_type = 'LparInfo'

    manage_editLparInfoForm = DTMLFile('dtml/manageEditLparInfo',globals())

    maxmem = -1
    minmem = -1
    onlinemem = -1
    lparnum = -1
    shared = -1 # 0=dedicated, 1=shared
    capped = -1 # 0=uncapped, 1=Capped
    smt = -1
    mincap = -1
    maxcap = -1
    entitledcap = -1
    weight = -1
    entitledpct = -1
    minvcpu = -1
    maxvcpu = -1
    vcpu = -1

    _properties = HWComponent._properties + (
                 {'id':'maxmem', 'type':'string', 'mode':'w'},
                 {'id':'minmem', 'type':'string', 'mode':'w'},
                 {'id':'lparnum', 'type':'string', 'mode':'w'},
                 {'id':'shared', 'type':'string', 'mode':'w'},
                 {'id':'capped', 'type':'string', 'mode':'w'},
                 {'id':'smt', 'type':'string', 'mode':'w'},
                 {'id':'mincap', 'type':'string', 'mode':'w'},
                 {'id':'maxcap', 'type':'string', 'mode':'w'},
                 {'id':'onlinemem', 'type':'string', 'mode':'w'},
                 {'id':'entitledcap', 'type':'string', 'mode':'w'},
                 {'id':'weight', 'type':'string', 'mode':'w'},
                 {'id':'entitledpct', 'type':'string', 'mode':'w'},
                 {'id':'vcpu', 'type':'string', 'mode':'w'},
                 {'id':'minvcpu', 'type':'string', 'mode':'w'},
                 {'id':'maxvcpu', 'type':'string', 'mode':'w'},
                )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXDeviceHW", "lparinfo")),
        )


    factory_type_information = (
        {
            'id'             : 'LparInfo',
            'meta_type'      : 'LparInfo',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addLparInfo',
            'immediate_view' : 'viewLparInfo',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewLparInfo'
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

    def smtstr(self):
        """
        Return the friendly smt status
        """
        if self.smt is 1:
            return "Enabled"
        if self.smt is 0:
            return "Disabled"
        if self.smt is -1:
            return "Unknown"

    def cappedstr(self):
        """
        Return the friendly smt status
        """
        if self.capped is 1:
            return "Capped"
        if self.capped is 0:
            return "UnCapped"
        if self.capped is -1:
            return "Unknown"

    def sharedstr(self):
        """
        Return the friendly smt status
        """
        if self.shared is 1:
            return "Shared"
        if self.shared is 0:
            return "Dedicated"
        if self.shared is -1:
            return "Unknown"


InitializeClass(AIXLparInfo)
