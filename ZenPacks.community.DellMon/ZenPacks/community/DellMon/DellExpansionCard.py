################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellExpansionCard

DellExpansionCard is an abstraction of a PCI card.

$Id: DellExpansionCard.py,v 1.0 2009/06/23 23:02:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.ExpansionCard import *
from DellComponent import *

class DellExpansionCard(ExpansionCard, DellComponent):
    """ExpansionCard object"""

    portal_type = meta_type = 'DellExpansionCard'

    slot = 0
    status = 1
    monitor = False    

    _properties = HWComponent._properties + (
        {'id':'slot', 'type':'int', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'DellExpansionCard',
            'meta_type'      : 'DellExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'DellMon',
            'factory'        : 'manage_addDellExpansionCard',
            'immediate_view' : 'viewDellExpansionCard',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellExpansionCard'
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


InitializeClass(DellExpansionCard)
