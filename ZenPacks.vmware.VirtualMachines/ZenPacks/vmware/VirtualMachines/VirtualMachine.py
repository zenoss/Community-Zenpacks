from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class VirtualMachine(DeviceComponent, ManagedEntity):
	"Virtual Machine Information"
	
	portal_type = meta_type = 'VirtualMachine'

	vmDisplayName = ""
	vmGuestOS = ""
	vmGuestState = ""
	vmState = ""
	vmVMID = -1
	snmpindex = -1

	_properties = (
		dict(id='vmDisplayName',	type='string',	**_kw),
		dict(id='vmGuestOS',		type='string',	**_kw),
		dict(id='vmGuestState', 	type='string',	**_kw),
		dict(id='vmState',	 	type='string',	**_kw),
		dict(id='vmVMID',	 	type='int',	**_kw),
	)

	_relations = (
		('host', ToOne(ToManyCont, 
		'ZenPacks.vmware.VirtualMachines.VirtualMachine', 
			'virtualmachines')
		),
	)

	# Screen action bindings (and tab definitions)
	factory_type_information = (
		{
			'id'             : 'VirtualMachine',
			'meta_type'      : 'Virtual Machine',
			'description'    : 'Virtual Machine Description',
			'icon'           : 'Device_icon.gif',
			'product'        : 'VirtualMachines',
			'factory'        : 'manage_addVirtualMachine',
			'immediate_view' : 'terminalPerformance',
			'actions'        :
			(
				{ 'id'            : 'perf'
				, 'name'          : 'perf'
				, 'action'        : 'virtualmachinePerformance'
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

	def snmpIgnore(self):
		return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
	

InitializeClass(VirtualMachine)
