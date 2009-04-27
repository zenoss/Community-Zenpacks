################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqFcaCntlr

cpqFcaCntlr is an abstraction of a HP FC Array Controller.

$Id: cpqFcaCntlr.py,v 1.0 2008/12/03 08:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from HPExpansionCard import *

class cpqFcaCntlr(HPExpansionCard):
    """HP Disk Array Controller object"""

    portal_type = meta_type = 'cpqFcaCntlr'

    model = ""
    FWRev = ""
    redundancyType = ""
    wwpn = ""
    wwnn = ""
    role = 1
    chassis = ""
    external = False
        
    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
	        2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
		3: (DOT_RED, SEV_CRITICAL, 'Offline'),
		4: (DOT_ORANGE, SEV_ERROR, 'Redundant Path Offline'),
		5: (DOT_RED, SEV_CRITICAL, 'Not Connected'),
		}

    # we monitor RAID Controllers
    monitor = True

    _properties = HPExpansionCard._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'redundancyType', 'type':'string', 'mode':'w'},
        {'id':'wwpn', 'type':'string', 'mode':'w'},
        {'id':'wwnn', 'type':'string', 'mode':'w'},
        {'id':'role', 'type':'int', 'mode':'w'},
        {'id':'chassis', 'type':'string', 'mode':'w'},
        {'id':'external', 'type':'boolean', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'cpqFcaCntlr',
            'meta_type'      : 'cpqFcaCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCpqFcaCntlr',
            'immediate_view' : 'viewCpqFcaCntlr',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqFcaCntlr'
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

    def boxIoSlot(self):
        return self.snmpindex.split('.')[-1]

    def roleString(self):
        roles = {1: 'other',
                2: 'Not Duplexed',
	        3: 'Active',
	        4: 'Backup',
	        }
        return roles.get(getattr(self, 'role', 1), roles[1])

InitializeClass(cpqFcaCntlr)
