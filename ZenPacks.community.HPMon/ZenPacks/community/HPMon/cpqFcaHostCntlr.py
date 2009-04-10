################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqFcaHostCntlr

cpqFcaHostCntlr is an abstraction of a HP FC Host Bus Adapter.

$Id: cpqFcaHostCntlr.py,v 1.0 2008/12/03 08:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from HPExpansionCard import HPExpansionCard

class cpqFcaHostCntlr(HPExpansionCard):
    """FCA Host Bus Adapter object"""

    portal_type = meta_type = 'cpqFcaHostCntlr'

    model = ""
    FWRev = ""
    ROMRev = ""
    wwpn = ""
    wwnn = ""
    
    statusmap = [(4, 3, 'other'),
	        (4, 3, 'other'),
	        (0, 0, 'Ok'),
		(3, 5, 'Failed'),
		(3, 5, 'Shutdown'),
		(2, 4, 'Loop Degraded'),
		(3, 5, 'Loop Failed'),
		(2, 4, 'Not Connected'),
		]

    # we monitor RAID Controllers
    monitor = True

    _properties = HPExpansionCard._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'ROMRev', 'type':'string', 'mode':'w'},
        {'id':'wwpn', 'type':'string', 'mode':'w'},
        {'id':'wwnn', 'type':'string', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'cpqFcaHostCntlr',
            'meta_type'      : 'cpqFcaHostCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCpqFcaHostCntlr',
            'immediate_view' : 'viewCpqFcaHostCntlr',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqFcaHostCntlr'
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

InitializeClass(cpqFcaHostCntlr)
