################################################################################
#
# This program is part of the IBM3584Mon Zenpack
# Copyright (C) 2009 Josh Baird
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBM3584AccessDevice

IBM3584AccessDevice is a component of a Tape Library Device

$Id: $"""

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenModel.HWComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *

from ZenPacks.community.deviceAdvDetail.HWStatus import *

class IBM3584AccessDevice(HWComponent, HWStatus):
    """IBM3584AccessDevice object"""

    portal_type = meta_type = 'IBM3584AccessDevice'

    status = 1
    devicetype = ""
    model = ""
    serial = ""
    firmware = ""
    needsCleaning = 2

    _properties = HWComponent._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
        {'id':'devicetype', 'type':'string', 'mode':'w'},
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'serial', 'type':'string', 'mode':'w'},
        {'id':'firmware', 'type':'string', 'mode':'w'},
        {'id':'needsCleaning', 'type':'int', 'mode':'w'},
    )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "ZenPacks.community.IBM3584Mon.IBM3584DeviceHW", "accessdevices")),
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
            'id'             : 'Access Device',
            'meta_type'      : 'Access Device',
            'description'    : """Arbitrary device grouping class""",
            'product'        : 'ZenModel',
            'factory'        : 'manage_addAccessDevice',
            'immediate_view' : 'viewIBM3584AccessDevice',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewIBM3584AccessDevice'
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

    def needsCleaningString(self):
        clstatusmap = {0: 'Unknown', 1: 'Yes', 2: 'No'}
        clstatus = self.cacheRRDValue('needsCleaning', 0)
        return clstatusmap.get(clstatus, 'Unknown')        

    def getRRDNames(self):
        """
        Return the datapoint name of this access device
        'needsCleaning_needsCleaning' and 'status_status'
        """
        return ['needsCleaning_needsCleaning', 'status_status']

    def getFriendlyStatus(self):
        """
        Returns the friendly status string (not the integer)
        """
        friendlyStatus = self.status
        fstatusmap ={0: 'Unknown', 1: 'Other', 2: 'Running', 3: 'Warning', 4: 'Testing', 5:'Unknown',
               6: 'Powered Off', 7: 'Offline', 8: 'Off Duty', 9: 'Degraded', 10: 'Not Installed',
              11: 'Install Error', 12: 'Power Save Unknown', 13: 'Power Save Low Power Mode',
              14: 'Power Save Standby', 15: 'Power Save Cycle', 16: 'Power Save Warning',
              17: 'Paused', 18: 'Not Ready',
              }
        fsmap = fstatusmap.get(friendlyStatus, 'Unknown')
        return fsmap

InitializeClass(IBM3584AccessDevice)

