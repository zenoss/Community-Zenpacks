################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqSm2Cntlr

cpqSm2Cntlr is an abstraction of a HP iLO Board.

$Id: cpqSm2Cntlr.py,v 1.1 2010/06/30 16:31:02 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from HPExpansionCard import *

class cpqSm2Cntlr(HPExpansionCard):
    """iLO Board object"""

    model = ""
    romRev = ""
    hwVer = ""
    systemId = ""
    macaddress = ""
    ipaddress = ""
    subnetmask = ""
    dnsName = ""

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
                2: (DOT_ORANGE, SEV_ERROR, 'No Data'),
                3: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                4: (DOT_YELLOW, SEV_WARNING, 'Offline Data'),
                }

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
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

    def getDeviceProductName(self):
        return self.device().hw.getProductName()

    def getDeviceProductLink(self):
        return self.device().hw.getProductLink()

InitializeClass(cpqSm2Cntlr)
