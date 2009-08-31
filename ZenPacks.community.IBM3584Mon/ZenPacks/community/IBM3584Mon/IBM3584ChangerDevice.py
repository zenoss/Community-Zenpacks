################################################################################
#
# This program is part of the IBM3584Mon Zenpack
# Copyright (C) 2009 Josh Baird
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBM3584ChangerDevice

IBM3584ChangerDevice is a component of a Tape Library Device

$Id: $"""

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenModel.HWComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *

from ZenPacks.community.deviceAdvDetail.HWStatus import *

class IBM3584ChangerDevice(HWComponent, HWStatus):
    """IBM3584ChangerDevice object"""

    portal_type = meta_type = 'IBM3584ChangerDevice'

    deviceid = ""
    mediaflipping = 0
    name = ""
    description = ""
    status = 0

    _properties = HWComponent._properties + (
        {'id':'deviceid', 'type':'string', 'mode':'w'},
        {'id':'mediaflipping', 'type':'string', 'mode':'w'},
        {'id':'name', 'type':'string', 'mode':'w'},
        {'id':'description', 'type':'string', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "ZenPacks.community.IBM3584Mon.IBM3584DeviceHW", "changerdevices")),
        )


    statusmap ={0: (DOT_GREY, SEV_WARNING, 'Unknown'),
               1: (DOT_GREY, SEV_WARNING, 'Other'),
               2: (DOT_GREEN, SEV_CLEAN, 'Running'),
               3: (DOT_YELLOW, SEV_WARNING, 'Warning'),
               4: (DOT_BLUE, SEV_INFO, 'Testing'),
               5: (DOT_GREY, SEV_INFO, 'Unknown'),
               6: (DOT_RED, SEV_CRITICAL, 'Powered Off'),
               7: (DOT_RED, SEV_CRITICAL, 'Offline'),
               8: (DOT_RED, SEV_CRITICAL, 'Off Duty'),
               9: (DOT_RED, SEV_CRITICAL, 'Degraded'),
              10: (DOT_RED, SEV_WARNING, 'Not Installed'),
              11: (DOT_ORANGE, SEV_ERROR, 'Install Error'),
              12: (DOT_YELLOW, SEV_WARNING, 'Power Save Unknown'),
              13: (DOT_YELLOW, SEV_WARNING, 'Power Save Low Power Mode'),
              14: (DOT_YELLOW, SEV_WARNING, 'Power Save Standby'),
              15: (DOT_YELLOW, SEV_WARNING, 'Power Save Cycle'),
              16: (DOT_YELLOW, SEV_WARNING, 'Power Save Warning'),
              17: (DOT_GREY, SEV_INFO, 'Paused'),
              18: (DOT_ORANGE, SEV_WARNING, 'Not Ready'),
              }

    factory_type_information = (
        {
            'id'             : 'Changer Device',
            'meta_type'      : 'Changer Device',
            'description'    : """Arbitrary device grouping class""",
            'product'        : 'ZenModel',
            'factory'        : 'manage_addChangerDevice',
            'immediate_view' : 'viewIBM3584ChangerDevice',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewIBM3584ChangerDevice'
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

    def getFriendlyMFStatus(self):
        """
        Returns the friendly status string (not the integer)
        """
        friendlyStatus = self.status
        fstatusmap ={0: 'Unknown', 1: 'Yes', 2: 'No' }
        fsmap = fstatusmap.get(friendlyStatus, 'Unknown')
        return fsmap

InitializeClass(IBM3584ChangerDevice)

