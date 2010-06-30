################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellHardDisk

DellHardDisk is an abstraction of a harddisk.

$Id: DellHardDisk.py,v 1.2 2010/06/30 21:58:56 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

import inspect
from Products.ZenUtils.Utils import convToUnits
from Products.ZenModel.HardDisk import *
from DellComponent import *

class DellHardDisk(HardDisk, DellComponent):
    """DellHardDisk object"""

    rpm = 0
    size = 0
    diskType = ""
    hotPlug = 0
    bay = 0
    FWRev = ""
    status = 1

    statusmap ={0: (DOT_GREY, SEV_WARNING, 'Unknown'),
                1: (DOT_GREEN, SEV_CLEAN, 'Ready'),
                2: (DOT_RED, SEV_CRITICAL, 'Failed'),
                3: (DOT_GREEN, SEV_CLEAN, 'Online'),
                4: (DOT_RED, SEV_CRITICAL, 'Offline'), 
                6: (DOT_ORANGE, SEV_ERROR, 'Degraded'),
                7: (DOT_YELLOW, SEV_WARNING, 'Recovering'),
                11: (DOT_ORANGE, SEV_ERROR, 'Removed'),
                15: (DOT_YELLOW, SEV_WARNING, 'Resynching'),
                24: (DOT_YELLOW, SEV_WARNING, 'Rebuilding'),
                25: (DOT_YELLOW, SEV_WARNING, 'No Media'),
                26: (DOT_YELLOW, SEV_WARNING, 'Formatting'),
                28: (DOT_YELLOW, SEV_WARNING, 'Diagnostics'),
                34: (DOT_ORANGE, SEV_ERROR, 'Predictive Failure'),
                35: (DOT_YELLOW, SEV_WARNING, 'Initializing'),
                39: (DOT_ORANGE, SEV_ERROR, 'Foreign'),
                40: (DOT_YELLOW, SEV_WARNING, 'Clear'),
                41: (DOT_ORANGE, SEV_ERROR, 'Unsupported'),
                53: (DOT_ORANGE, SEV_ERROR, 'Incompatible'),
                }


    _properties = HardDisk._properties + (
                 {'id':'rpm', 'type':'int', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
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
            'immediate_view' : 'viewDellHardDisk',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellHardDisk'
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


    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size,divby=1000)

    def rpmString(self):
        """
        Return the RPM in tradition form ie 7200, 10K
        """
        if int(self.rpm) == 1:
            return 'Unknown'
        if int(self.rpm) < 10000:
            return int(self.rpm)
        else:
            return "%sK" %(int(self.rpm) / 1000)

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(DellHardDisk)
