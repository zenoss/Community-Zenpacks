from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class BlueArcClusterNode(DeviceComponent, ManagedEntity):
	"BlueArc Cluster Node Information"
	
	portal_type = meta_type = 'BlueArcClusterNode'

	nodeName = ""
	nodeID     = -1
	snmpindex  = -1

	_properties = (
		dict(id='nodeName',	type='string',	**_kw),
		dict(id='nodeID',	 	type='int',	**_kw),
	)

	_relations = (
		('host', ToOne(ToManyCont, 
		'ZenPacks.DrD_Studios.BlueArc.BlueArc', 
			'nodes')
		),
	)

	# Screen action bindings (and tab definitions)
	factory_type_information = (
		{
			'id'             : 'BlueArc',
			'meta_type'      : 'BlueArc Cluster Node',
			'description'    : 'Cluster Node Description',
			'icon'           : 'Device_icon.gif',
			'product'        : 'BlueArc',
			'factory'        : 'manage_addBlueArcClusterNode',
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
		return self.host()

	def managedDeviceLink(self):
		from Products.ZenModel.ZenModelRM import ZenModelRM
		d = self.getDmdRoot("Devices").findDevice(self.nodeName)
		if d:
			return ZenModelRM.urlLink(d, 'link')
		return None

	def snmpIgnore(self):
		return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
	

InitializeClass(BlueArcClusterNode)
