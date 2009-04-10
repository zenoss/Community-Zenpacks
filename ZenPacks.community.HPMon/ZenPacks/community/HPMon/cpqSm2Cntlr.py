################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqSm2Cntlr

cpqSm2Cntlr is an abstraction of a HP iLO Board.

$Id: cpqSm2Cntlr.py,v 1.0 2008/12/15 14:31:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from HPExpansionCard import HPExpansionCard

class cpqSm2Cntlr(HPExpansionCard):
    """iLO Board object"""

    portal_type = meta_type = 'cpqSm2Cntlr'

    model = ""
    romRev = ""
    hwVer = ""
    systemId = ""
    macaddress = ""
    ipaddress = ""
    subnetmask = ""
    dnsName = ""
    
    statusmap = [(4, 3, 'other'),
	        (4, 3, 'other'),
	        (2, 4, 'No Data'),
	        (0, 0, 'Ok'),
		(1, 3, 'Offline Data'),
		]

    # we monitor RAID Controllers
    monitor = True

    _properties = HPExpansionCard._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'romRev', 'type':'string', 'mode':'w'},
        {'id':'hwVer', 'type':'string', 'mode':'w'},
        {'id':'systemId', 'type':'string', 'mode':'w'},
        {'id':'macaddress', 'type':'string', 'mode':'w'},
        {'id':'ipaddress', 'type':'string', 'mode':'w'},
        {'id':'subnetmask', 'type':'string', 'mode':'w'},
        {'id':'dnsName', 'type':'string', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'cpqSm2Cntlr',
            'meta_type'      : 'cpqSm2Cntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCpqSm2Cntlr',
            'immediate_view' : 'viewCpqSm2Cntlr',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqSm2Cntlr'
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

InitializeClass(cpqSm2Cntlr)
