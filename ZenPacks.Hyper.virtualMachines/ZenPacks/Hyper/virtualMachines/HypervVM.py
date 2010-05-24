from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class HypervVM(DeviceComponent, ManagedEntity):
	"Virtual Machine Information"
	
	portal_type = meta_type = 'HypervVM'

	vmDisplayName = ""
	vmMemory = ""
	vmState = ""
	vmVMID = -1
	snmpindex = -1

	_properties = (
		dict(id='vmDisplayName',	type='string',	**_kw),
		dict(id='vmMemory',		type='string',	**_kw),
		dict(id='vmState',	 	type='string',	**_kw),
		dict(id='vmVMID',	 	type='int',	**_kw),
	)

	_relations = (
		('host', ToOne(ToManyCont, 
		'ZenPacks.Hyper.virtualMachines.HypervVM', 
			'HypervVM')
		),
	)

	# Screen action bindings (and tab definitions)
	factory_type_information = (
		{
			'id'             : 'HypervVM',
			'meta_type'      : 'Virtual Machine',
			'description'    : 'Hyper-V Virtual Machine Description',
			'icon'           : 'Device_icon.gif',
			'product'        : 'HypervVM',
			'factory'        : 'manage_addVirtualMachine',
			'immediate_view' : 'HypervVMPerformance',
			'actions'        :
			(
				{ 'id'            : 'perf'
				, 'name'          : 'perf'
				, 'action'        : 'HyperVMPerformance'
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
		d = self.getDmdRoot("Devices").findDevice(self.vmDisplayName)
		if d:
			return ZenModelRM.urlLink(d, 'link')
		return None


InitializeClass(HypervVM)
