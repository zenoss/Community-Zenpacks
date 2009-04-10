################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPLogicalDisk

HPLogicalDisk is an abstraction of a harddisk.

$Id: HPLogicalDisk.py,v 1.0 2008/12/09 15:05:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.HardDisk import *
from HPComponent import HPComponent

class HPLogicalDisk(HardDisk, HPComponent):
    """HPLogicalDisk object"""

    size = 0
    stripesize = 0
    diskType = ""
    status = 1

    _properties = HWComponent._properties + (
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'stripesize', 'type':'int', 'mode':'w'},
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
            'immediate_view' : 'viewHPLogicalDisk',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPLogicalDisk'
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


    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size,divby=1000)

    def stripesizeString(self):
        """
        Return the Stripes Size in human readable form ie 64Kb
        """
        return convToUnits(self.stripesize)

InitializeClass(HPLogicalDisk)
