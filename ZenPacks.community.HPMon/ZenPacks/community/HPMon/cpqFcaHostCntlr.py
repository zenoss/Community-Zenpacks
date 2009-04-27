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

from HPExpansionCard import *

class cpqFcaHostCntlr(HPExpansionCard):
    """FCA Host Bus Adapter object"""

    portal_type = meta_type = 'cpqFcaHostCntlr'

    model = ""
    FWRev = ""
    ROMRev = ""
    wwpn = ""
    wwnn = ""
    
    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
	        2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
		3: (DOT_RED, SEV_CRITICAL, 'Failed'),
		4: (DOT_RED, SEV_CRITICAL, 'Shutdown'),
		5: (DOT_ORANGE, SEV_ERROR, 'Loop Degraded'),
		6: (DOT_RED, SEV_CRITICAL, 'Loop Failed'),
		7: (DOT_ORANGE, SEV_ERROR, 'Not Connected'),
		}

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
