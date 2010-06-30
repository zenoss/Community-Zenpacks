################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellExpansionCard

DellExpansionCard is an abstraction of a PCI card.

$Id: DellExpansionCard.py,v 1.1 2010/06/30 21:57:58 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.ExpansionCard import *
from DellComponent import *

class DellExpansionCard(ExpansionCard, DellComponent):
    """ExpansionCard object"""

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

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(DellExpansionCard)
