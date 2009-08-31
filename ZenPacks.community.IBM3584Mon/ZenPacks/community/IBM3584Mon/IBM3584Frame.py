################################################################################
#
# This program is part of the IBM3584Mon Zenpack
# Copyright (C) 2009 Josh Baird
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBM3584Frame

IBM3584Frame is a component of a Tape Library Device

$Id: $"""

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenModel.HWComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *

from ZenPacks.community.deviceAdvDetail.HWStatus import *

class IBM3584Frame(HWComponent, HWStatus):
    """IBM3584Frame object"""

    portal_type = meta_type = 'IBM3584Frame'

    status = 1
    model = ""
    serial = ""
    frametype = ""

    _properties = HWComponent._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'serial', 'type':'string', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
        {'id':'frametype', 'type':'string', 'mode':'w'},
    )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "ZenPacks.community.IBM3584Mon.IBM3584DeviceHW", "frames")),
        )


    statusmap ={0: (DOT_GREY, SEV_WARNING, 'Unknown'),
                1: (DOT_GREY, SEV_WARNING, 'Other'),
                2: (DOT_GREEN, SEV_CLEAN, 'OK'),
                3: (DOT_RED, SEV_CRITICAL, 'Degraded'),
                4: (DOT_YELLOW, SEV_WARNING, 'Stressed'),
                5: (DOT_YELLOW, SEV_WARNING, 'Predictive Failure'),
                6: (DOT_ORANGE, SEV_ERROR, 'Error'),
                7: (DOT_RED, SEV_CRITICAL, 'Not Recoverable'),
                8: (DOT_YELLOW, SEV_WARNING, 'Starting'),
                9: (DOT_YELLOW, SEV_WARNING, 'Stopping'),
               10: (DOT_RED, SEV_CRITICAL, 'Stopped'),
               11: (DOT_GREEN, SEV_CLEAN, 'In Service'),
               12: (DOT_ORANGE, SEV_WARNING, 'Aborted'),
               }

    factory_type_information = (
        {
            'id'             : 'Frame',
            'meta_type'      : 'Frame',
            'description'    : """Arbitrary device grouping class""",
            'product'        : 'ZenModel',
            'factory'        : 'manage_addFrame',
            'immediate_view' : 'viewIBM3584Frame',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewIBM3584Frame'
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

    def getFriendlyFrameStatus(self):
        """
        Returns the friendly status string (not the integer)
        """
        ffriendlyStatus = self.status
        ffstatusmap ={0: 'Unknown', 1: 'Other', 2: 'OK', 3: 'Degraded', 4: 'Stressed', 5:'Predictive Failure',
               6: 'Error', 7: 'Non Recoverable Error', 8: 'Starting', 9: 'Stopping', 10: 'Stopped',
              11: 'In Service', 12: 'No Contact', 13: 'Lost Communication',
              14: 'Aborted', 15: 'Dormant', 16: 'Supporting Entity in Error',
              17: 'Completed', 18: 'Power Mode',
              }
        ffsmap = ffstatusmap.get(ffriendlyStatus, 'Unknown')
        return ffsmap

    def getRRDNames(self):
        """
        Return the datapoint name of this access device
        'status_status'
        """
        return ['status_status']


InitializeClass(IBM3584Frame)

