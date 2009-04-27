################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqIdeController

cpqIdeController is an abstraction of a HP IDE Controller.

$Id: cpqIdeController.py,v 1.0 2008/12/09 14:31:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from HPExpansionCard import *

class cpqIdeController(HPExpansionCard):
    """IDE Controller object"""

    portal_type = meta_type = 'cpqIdeController'

    model = ""
    FWRev = ""

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
	        2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
		3: (DOT_RED, SEV_CRITICAL, 'Failed'),
		}
    
    # we monitor RAID Controllers
    monitor = True

    _properties = HPExpansionCard._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'FWRev', 'type':'string', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'cpqIdeController',
            'meta_type'      : 'cpqIdeController',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCpqIdeController',
            'immediate_view' : 'viewCpqIdeController',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqIdeController'
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

InitializeClass(cpqIdeController)
