################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqDaCntlr

cpqDaCntlr is an abstraction of a HP Smart Array Controller.

$Id: cpqDaCntlr.py,v 1.0 2008/12/04 10:13:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from HPExpansionCard import HPExpansionCard

class cpqDaCntlr(HPExpansionCard):
    """Disk Aray Controller object"""

    portal_type = meta_type = 'cpqDaCntlr'

    model = ""
    FWRev = ""
    role = 1
    redundancyType = ""
    
    # we monitor RAID Controllers
    monitor = True

    statusmap = [(4, 3, 'other'),
	        (4, 3, 'other'),
		(0, 0, 'Ok'),
		(3, 5, 'General Failure'),
		(2, 4, 'Cable Problem'),
		(3, 5, 'Powered Off'),
		]
		
    _properties = HPExpansionCard._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'role', 'type':'int', 'mode':'w'},
        {'id':'redundancyType', 'type':'string', 'mode':'w'},
    )


    factory_type_information = ( 
        { 
            'id'             : 'cpqDaCntlr',
            'meta_type'      : 'cpqDaCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCpqDaCntlr',
            'immediate_view' : 'viewCpqDaCntlr',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqDaCntlr'
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

    def roleString(self):
        roles = {1: 'other',
                2: 'Not Duplexed',
	        3: 'Active',
	        4: 'Backup',
	        }
        return roles.get(self.role, roles[1])

InitializeClass(cpqDaCntlr)
