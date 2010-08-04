from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenRelations.RelSchema import *

import copy

class Cluster(Device):
	"BlueArc Cluster"

	_relations = Device._relations + (
		('nodes', ToManyCont(ToOne, 
			"ZenPacks.DrD_Studios.BlueArc.ClusterNode", "cluster")),
		)
	
	factory_type_information = (
			{
				'immediate_view' : 'deviceStatus',
				'actions'        :
				(
					{ 'id'            : 'status'
					, 'name'          : 'Status'
					, 'action'        : 'deviceStatus'
					, 'permissions'   : (ZEN_VIEW, )
					},
					{ 'id'            : 'osdetail'
					, 'name'          : 'OS'
					, 'action'        : 'deviceOsDetail'
					, 'permissions'   : (ZEN_VIEW, )
					},
					{ 'id'            : 'nodeData'
					, 'name'          : 'Cluster Nodes'
					, 'action'        : 'nodeData'
					, 'permissions'   : (ZEN_VIEW,)
					},
					{ 'id'            : 'hwdetail'
					, 'name'          : 'Hardware'
					, 'action'        : 'deviceHardwareDetail'
					, 'permissions'   : (ZEN_VIEW, )
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

InitializeClass(Cluster)
