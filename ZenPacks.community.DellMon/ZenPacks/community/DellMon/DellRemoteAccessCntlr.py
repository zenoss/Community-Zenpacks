################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellRemoteAccessCntlr

DellRemoteAccessCntlr is an abstraction of a Dell DRAC Controller.

$Id: DellRemoteAccessCntlr.py,v 1.2 2010/11/15 17:30:16 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from DellExpansionCard import *

class DellRemoteAccessCntlr(DellExpansionCard):
    """Delll DRAC Controller object"""

    FWRev = ""
    SWVer = ""
    ipaddress = ""
    macaddress = ""
    subnetmask = ""

    # we monitor DRAC Controllers
    monitor = True

    _properties = DellExpansionCard._properties + (
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'SWVer', 'type':'string', 'mode':'w'},
        {'id':'ipaddress', 'type':'string', 'mode':'w'},
        {'id':'macaddress', 'type':'string', 'mode':'w'},
        {'id':'subnetmask', 'type':'string', 'mode':'w'},
    )


    factory_type_information = (
        {
            'id'             : 'DellRemoteAccessCntlr',
            'meta_type'      : 'DellRemoteAccessCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addDellRemoteAccessCntlr',
            'immediate_view' : 'viewDellRemoteAccessCntlr',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellRemoteAccessCntlr'
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

InitializeClass(DellRemoteAccessCntlr)
