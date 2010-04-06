from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenRelations.RelSchema import *

import copy

class BladeChassis(Device):
    "HP Blade Chassis Device"

    _relations = Device._relations + (
	('bladeservers', ToManyCont(ToOne, "ZenPacks.community.HPBladeChassis.BladeServer", "bladechassis")),
    ) + (
	('bladechassisfans', ToManyCont(ToOne, "ZenPacks.community.HPBladeChassis.BladeChassisFan", "bladechassis")),
    ) + (
	('bladechassisinterconnects', ToManyCont(ToOne, "ZenPacks.community.HPBladeChassis.BladeChassisInterconnect", "bladechassis")),
    ) + (
	('bladechassispsus', ToManyCont(ToOne, "ZenPacks.community.HPBladeChassis.BladeChassisPsu", "bladechassis")),
    ) 
    

    
    factory_type_information = (
	{
	    'immediate_view' : 'deviceStatus',
	    'actions'        : (
		{ 'id'            : 'status'
		, 'name'          : 'Status'
		, 'action'        : 'deviceStatus'
		, 'permissions'   : (ZEN_VIEW, )
		},
		{ 'id'            : 'bladechassisData'
		, 'name'          : 'Chassis Details'
		, 'action'        : 'bladechassisData'
		, 'permissions'   : (ZEN_VIEW,)
		},
		{ 'id'            : 'bladeserverData'
		, 'name'          : 'Blades'
		, 'action'        : 'bladeserverData'
		, 'permissions'   : (ZEN_VIEW,)
		},
		{ 'id'            : 'events'
		, 'name'          : 'Events'
		, 'action'        : 'viewEvents'
		, 'permissions'   : (ZEN_VIEW, )
		},
		{ 'id'            : 'perfServer'
		, 'name'          : 'Perf'
		, 'action'        : 'viewDevicePerformance'
		, 'permissions'   : (ZEN_VIEW, )
		},
		{ 'id'            : 'edit'
		, 'name'          : 'Edit'
		, 'action'        : 'editDevice'
		, 'permissions'   : ("Change Device",)
		},
	    )
	},
    )

InitializeClass(BladeChassis)
