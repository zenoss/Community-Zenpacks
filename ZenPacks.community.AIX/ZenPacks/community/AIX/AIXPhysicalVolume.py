from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from Products.ZenRelations.RelSchema import *
from Products.ZenUtils.Utils import prepId
from Products.ZenModel.OSComponent import OSComponent
import copy

def manage_addPhysicalVolume(context, id, userCreated, REQUEST=None):
    """make a physicalvolume"""
    pvid = prepId(id)
    pv = AIXPhysicalVolume(pvid)
    context._setObject(pvid, pv)
    pv = context._getOb(pvid)
    if userCreated: pv.setUserCreateFlag()
    if REQUEST is not None:
       REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return pv

#addLogicalVolume = DTMLFile('dtml/addLogicalVolume',globals())


class AIXPhysicalVolume(OSComponent):
    "Aix Physical Volume class"

    # Set so a template named PrintQueue will bind automatically
    portal_type = meta_type = 'PhysicalVolume'

    # Attribute Defaults
    title = ""
    aixPvState = ""
    aixPvNameVg = ""
    aixPvSize = ""
    aixPvFree = ""
    aixPvNumLVs = ""

    # Define New Properties for this class
    _properties = OSComponent._properties + (
        {'id':'title', 'type':'string', 'mode':''},
        {'id':'aixPvState', 'type':'string', 'mode':''},
        {'id':'aixPvNameVg', 'type':'string', 'mode':''},
        {'id':'aixPvSize', 'type':'string', 'mode':''},
        {'id':'aixPvFree', 'type':'string', 'mode':''},
        {'id':'aixPvNumLVs', 'type':'string', 'mode':''},
    )

    # Define new relationships
    _relations = (
    ('volumegroup', ToOne(ToManyCont, 'ZenPacks.community.AIX.AIXVolumeGroup', 'physicalvolume')),
        )

    # Define tabs and screen templates to use when this component is selected
    factory_type_information = (
        {
            'id'             : 'PhysicalVolume',
            'meta_type'      : 'PhysicalVolume',
            'description'    : """physical volume grouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addPhysicalVolume',
            'immediate_view' : 'viewPhysicalVolume',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewPhysicalVolume'
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

InitializeClass(AIXPhysicalVolume)
