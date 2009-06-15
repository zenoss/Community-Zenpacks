__doc__="""AIX ExpansionCard
"""

from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *

from Products.ZenModel.HWComponent import HWComponent
from Products.ZenModel.ExpansionCard import ExpansionCard

from Products.ZenModel.ZenossSecurity import *

class AIXExpansionCard(ExpansionCard):
    """AIX ExpansionCard object"""

    # we don't monitor cards
    # monitor = False

    #_properties = ExpansionCard._properties + (
    #    {'id':'slot', 'type':'int', 'mode':'w'},
    #)

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXDeviceHW", "cards")),
        )


    factory_type_information = (
        {
            'id'             : 'AIXExpansionCard',
            'meta_type'      : 'AIXExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addAIXExpansionCard',
            'immediate_view' : 'viewAIXExpansionCard',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewAIXExpansionCard'
                , 'permissions'   : ('View',)
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

InitializeClass(AIXExpansionCard)
