################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPPowerSupply

HPPowerSupply is an abstraction of a PowerSupply.

$Id: HPPowerSupply.py,v 1.0 2008/11/28 15:32:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.PowerSupply import *
from HPComponent import *

class HPPowerSupply(PowerSupply, HPComponent):
    """PowerSupply object"""

    portal_type = meta_type = 'HPPowerSupply'

    status = 1
    
    statusmap ={1: (DOT_GREEN, SEV_CLEAN, 'No Error'),
		2: (DOT_RED, SEV_CRITICAL, 'General Failure'),
		3: (DOT_RED, SEV_CRITICAL, 'Bist Failure'),
		4: (DOT_ORANGE, SEV_ERROR, 'Fan Failure'),
		5: (DOT_ORANGE, SEV_ERROR, 'Temperature Failure'),
		6: (DOT_ORANGE, SEV_ERROR, 'Interlock Open'),
		7: (DOT_ORANGE, SEV_ERROR, 'EPROM Failure'),
		8: (DOT_ORANGE, SEV_ERROR, 'VREF Failed'),
		9: (DOT_ORANGE, SEV_ERROR, 'DAC Failed'),
		10:(DOT_ORANGE, SEV_ERROR, 'RAM Test Failed'),
		11:(DOT_ORANGE, SEV_ERROR, 'Voltage Channel Failed'),
		12:(DOT_RED, SEV_CRITICAL, 'Brown Out'),
		13:(DOT_ORANGE, SEV_ERROR, 'Giveup on Startup'),
		14:(DOT_RED, SEV_CRITICAL, 'NVRAM Invalid'),
		15:(DOT_ORANGE, SEV_ERROR, 'Calibration Table Invalid'),
		}

    _properties = HWComponent._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'PowerSupply',
            'meta_type'      : 'PowerSupply',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'PowerSupply_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addPowerSupply',
            'immediate_view' : 'viewHPPowerSupply',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPPowerSupply'
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
	
    def state(self):
        return self.statusString()

InitializeClass(HPPowerSupply)
