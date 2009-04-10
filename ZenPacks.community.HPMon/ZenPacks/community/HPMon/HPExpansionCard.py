################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPExpansionCard

HPExpansionCard is an abstraction of a PCI card.

$Id: HPExpansionCard.py,v 1.0 2008/12/03 08:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.ExpansionCard import *
from HPComponent import HPComponent

class HPExpansionCard(ExpansionCard, HPComponent):
    """ExpansionCard object"""
    slot = 0
    status = 1
    
    # we don't monitor cards
    monitor = False

    _properties = HWComponent._properties + (
        {'id':'slot', 'type':'int', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'ExpansionCard',
            'meta_type'      : 'ExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addExpansionCard',
            'immediate_view' : 'viewHPExpansionCard',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPExpansionCard'
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

InitializeClass(HPExpansionCard)
