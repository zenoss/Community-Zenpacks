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
from HPComponent import HPComponent

class HPPowerSupply(PowerSupply, HPComponent):
    """PowerSupply object"""

    portal_type = meta_type = 'HPPowerSupply'

    status = 1
    
    statusmap = [(4, 3, 'Other'),
	        (0, 0, 'No Error'),
		(3, 5, 'General Failure'),
		(3, 5, 'Bist Failure'),
		(2, 4, 'Fan Failure'),
		(2, 4, 'Temperature Failure'),
		(2, 4, 'Interlock Open'),
		(2, 4, 'EPROM Failure'),
		(2, 4, 'VREF Failed'),
		(2, 4, 'DAC Failed'),
		(2, 4, 'RAM Test Failed'),
		(2, 4, 'Voltage Channel Failed'),
		(3, 5, 'Brown Out'),
		(2, 4, 'Giveup on Startup'),
		(3, 5, 'NVRAM Invalid'),
		(2, 4, 'Calibration Table Invalid'),
		]

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
