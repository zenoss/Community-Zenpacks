################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqSePciSlot

cpqSePciSlot is an abstraction of a PCI Slot.

$Id: cpqSePciSlot.py,v 1.1 2010/06/30 16:30:10 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from HPExpansionCard import *

class cpqSePciSlot(HPExpansionCard):
    """PCI Slot object"""

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
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

InitializeClass(cpqSePciSlot)
