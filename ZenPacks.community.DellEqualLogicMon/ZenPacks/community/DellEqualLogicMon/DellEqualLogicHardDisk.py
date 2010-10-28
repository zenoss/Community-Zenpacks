################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################\

import inspect
from Products.ZenModel.HardDisk import *
from ZenPacks.community.deviceAdvDetail.HWStatus import *

class DellEqualLogicHardDisk(HardDisk, HWStatus):

    size = 0
    diskType = ""
    hotPlug = 0
    bay = 0
    FWRev = ""
    status = 1

    statusmap ={1: (DOT_GREEN, SEV_CLEAN, 'Online'),
                2: (DOT_GREEN, SEV_CLEAN, 'Spare'),
                3: (DOT_RED, SEV_CRITICAL, 'failed'),
                4: (DOT_RED, SEV_CRITICAL, 'Offline'),
                5: (DOT_YELLOW, SEV_WARNING, 'Alt-sig'),
		6: (DOT_YELLOW, SEV_WARNING, 'Too Small'),
                7: (DOT_YELLOW, SEV_WARNING, 'History of failures'),
		8: (DOT_ORANGE, SEV_ERROR, 'Unsupported version'),
		9: (DOT_ORANGE, SEV_ERROR, 'Unhealthy'),
		10: (DOT_GREEN, SEV_CLEAN, 'Replacement'),
                }


    _properties = HardDisk._properties + (
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'bay', 'type':'int', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
                 {'id':'status', 'type':'int', 'mode':'w'},
                )

    factory_type_information = (
        {
            'id'             : 'HardDisk',
            'meta_type'      : 'HardDisk',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewDellEqualLogicHardDisk',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellEqualLogicHardDisk'
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

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(DellEqualLogicHardDisk)
