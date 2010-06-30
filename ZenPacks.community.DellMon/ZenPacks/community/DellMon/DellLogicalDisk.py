################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellLogicalDisk

DellLogicalDisk is an abstraction of a harddisk.

$Id: DellLogicalDisk.py,v 1.2 2010/06/30 22:00:33 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.LogicalDisk import *
from DellComponent import *

class DellLogicalDisk(LogicalDisk, DellComponent):
    """DellLogicalDisk object"""

    statusmap ={0: (DOT_GREY, SEV_WARNING, 'Unknown'),
                1: (DOT_GREEN, SEV_CLEAN, 'Ready'),
                2: (DOT_RED, SEV_CRITICAL, 'Failed'),
                3: (DOT_GREEN, SEV_CLEAN, 'Online'),
                4: (DOT_RED, SEV_CRITICAL, 'Offline'), 
                6: (DOT_ORANGE, SEV_ERROR, 'Degraded'),
                15: (DOT_YELLOW, SEV_WARNING, 'Resynching'),
                16: (DOT_YELLOW, SEV_WARNING, 'Regenerating'),
                24: (DOT_YELLOW, SEV_WARNING, 'Rebuilding'),
                26: (DOT_YELLOW, SEV_WARNING, 'Formatting'),
                32: (DOT_YELLOW, SEV_WARNING, 'Reconstructing'),
                35: (DOT_YELLOW, SEV_WARNING, 'Initializing'),
                36: (DOT_YELLOW, SEV_WARNING, 'Background Initialization'),
                38: (DOT_YELLOW, SEV_WARNING, 'Resynching Paused'),
                52: (DOT_RED, SEV_CRITICAL, 'Permanently Degraded'),
                54: (DOT_ORANGE, SEV_ERROR, 'Degraded Redundancy'),
                }


    factory_type_information = (
        {
            'id'             : 'HardDisk',
            'meta_type'      : 'HardDisk',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewDellLogicalDisk',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellLogicalDisk'
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

InitializeClass(DellLogicalDisk)
