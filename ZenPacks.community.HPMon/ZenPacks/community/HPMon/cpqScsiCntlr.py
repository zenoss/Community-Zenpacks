################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqScsiCntlr

cpqScsiCntlr is an abstraction of a HP SCSI Controller.

$Id: cpqScsiCntlr.py,v 1.0 2008/12/09 10:51:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from HPExpansionCard import *

class cpqScsiCntlr(HPExpansionCard):
    """SCSI Cntrl object"""

    portal_type = meta_type = 'cpqScsiCntlr'

    model = ""
    FWRev = ""
    scsiwidth = ""

    # we monitor RAID Controllers
    monitor = True

    _properties = HPExpansionCard._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'scsiwidth', 'type':'string', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'cpqScsiCntlr',
            'meta_type'      : 'cpqScsiCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCpqScsiCntlr',
            'immediate_view' : 'viewCpqScsiCntlr',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqScsiCntlr'
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

InitializeClass(cpqScsiCntlr)
