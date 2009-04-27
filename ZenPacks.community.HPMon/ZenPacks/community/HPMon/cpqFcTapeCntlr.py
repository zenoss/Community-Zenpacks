################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqFcTapeCntlr

cpqFcTapeCntlr is an abstraction of a HP FC Tape Controller.

$Id: cpqFcTapeCntlr.py,v 1.0 2008/12/03 08:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from HPExpansionCard import *

class cpqFcTapeCntlr(HPExpansionCard):
    """HP Fibre Channel Tape Controller object"""

    portal_type = meta_type = 'cpqFcTapeCntlr'

    model = ""
    FWRev = ""
    wwnn = ""
        
    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
	        2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
		3: (DOT_RED, SEV_CRITICAL, 'Offline'),
		}

    # we monitor RAID Controllers
    monitor = True

    _properties = HPExpansionCard._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'wwnn', 'type':'string', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'cpqFcTapeCntlr',
            'meta_type'      : 'cpqFcTapeCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCpqFcTapeCntlr',
            'immediate_view' : 'viewCpqFcTapeCntlr',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqFcTapeCntlr'
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

InitializeClass(cpqFcTapeCntlr)
