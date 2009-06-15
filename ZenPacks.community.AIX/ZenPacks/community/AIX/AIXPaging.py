__doc__="""AIXPaging
AIXPaging is a paging volume on an aix server
"""

import logging
log = logging.getLogger("zen.AIXPaging")

from Globals import DTMLFile
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenUtils.Utils import prepId
from Products.ZenUtils.Utils import convToUnits
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.OSComponent import OSComponent
from Products.ZenWidgets import messaging
from Products.ZenModel.ZenossSecurity import *
import copy

def manage_addPaging(context, id, userCreated, REQUEST=None):
    """make a paging volume"""
    pageid = prepId(id)
    page = AIXPaging(pageid)
    context._setObject(pageid, page)
    page = context._getOb(pageid)
    if userCreated: page.setUserCreateFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return page

addPaging = DTMLFile('dtml/addPaging',globals())

class AIXPaging(OSComponent):
    """
    AIXPaging object
    """

    portal_type = meta_type = 'Paging'

    manage_editFileSystemForm = DTMLFile('dtml/manageEditPaging',globals())

    aixPageName = ""
    aixPageNameVg = ""
    aixPageNamePv = ""
    aixPageSize = ""
    aixPagePercentUsed = ""
    aixPageStatus = ""
    aixPageType = ""

    security = ClassSecurityInfo()

    _properties = OSComponent._properties + (
        {'id':'aixPageName', 'type':'string', 'mode':''},
        {'id':'aixPageNameVg', 'type':'string', 'mode':''},
        {'id':'aixPageNamePv', 'type':'string', 'mode':''},
        {'id':'aixPageSize', 'type':'string', 'mode':''},
        {'id':'aixPagePercentUsed', 'type':'string', 'mode':''},
        {'id':'aixPageStatus', 'type':'string', 'mode':''},
        {'id':'aixPageType', 'type':'string', 'mode':''},
        )

    _relations = OSComponent._relations + (
        ("logicalvolume", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXLogicalVolume", "paging")),
        )


    factory_type_information = (
        {
            'id'             : 'Paging',
            'meta_type'      : 'Paging',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addPaging',
            'immediate_view' : 'viewPaging',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewPaging'
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

InitializeClass(AIXPaging)
