################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPHardDisk

HPHardDisk is an abstraction of a harddisk.

$Id: HPHardDisk.py,v 1.1 2010/06/29 10:37:31 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.HardDisk import *
from HPComponent import *

class HPHardDisk(HardDisk, HPComponent):
    """HPHardDisk object"""

    rpm = 0
    size = 0
    diskType = ""
    hotPlug = 0
    bay = 0
    FWRev = ""
    status = 1

    _properties = HWComponent._properties + (
                 {'id':'rpm', 'type':'int', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'hotPlug', 'type':'int', 'mode':'w'},
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
            'immediate_view' : 'viewHPHardDisk',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPHardDisk'
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

    def hotPlugString(self):
        """
        Return the HotPlug Status
        """
        if self.hotPlug == 2:
            return 'HotPlug'
        if self.hotPlug == 3:
            return 'nonHotPlug'
        return 'other'

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(HPHardDisk)
