from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class ClusterNode(DeviceComponent, ManagedEntity):
	"BlueArc Cluster Node Information"
	
	portal_type = meta_type = 'ClusterNode'

	snmpindex  = -1
	nodeID     = -1
	nodeName   = ""
	nodeIP     = ""
	nodeStatus = ""

	_properties = (
		dict(id='nodeID',	 	  type='int',	**_kw),
		dict(id='nodeName',	  type='string',	**_kw),
		dict(id='nodeIP',	 	  type='string',	**_kw),
		dict(id='nodeStatus',	type='string',	**_kw),
	)

	_relations = (
		('cluster', ToOne(ToManyCont, 
		'ZenPacks.DrD_Studios.BlueArc.ClusterNode', 
			'nodes')
		),
	)

	# Screen action bindings (and tab definitions)
	factory_type_information = (
		{
			'id'             : 'Node',
			'meta_type'      : 'BlueArc Cluster Node',
			'description'    : 'Cluster Node Description',
			'icon'           : 'Device_icon.gif',
			'product'        : 'BlueArc',
			'factory'        : 'manage_addClusterNode',
			'immediate_view' : 'nodePerformance',
			'actions'        :
			(
				{ 'id'            : 'perf'
				, 'name'          : 'perf'
				, 'action'        : 'nodePerformance'
				, 'permissions'   : (ZEN_VIEW, )
				},
				{ 'id'            : 'templates'
				, 'name'          : 'Templates'
				, 'action'        : 'objTemplates'
				, 'permissions'   : (ZEN_CHANGE_SETTINGS, )
				},
			)
		},
	)

	def device(self):
		return self.cluster()

	def managedDeviceLink(self):
		from Products.ZenModel.ZenModelRM import ZenModelRM
		d = self.getDmdRoot("Devices").findDevice(self.nodeName)
		if d:
			return ZenModelRM.urlLink(d, 'link')
		return None

	def snmpIgnore(self):
		return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
	

InitializeClass(ClusterNode)
