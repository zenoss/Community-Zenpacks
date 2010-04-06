from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class BladeChassisPsu(DeviceComponent, ManagedEntity):
    "Blade Chassis PSU Information"
    
    portal_type = meta_type = 'BladeChassisPsu'

    bcpNumber = -1
    bcpProductName = ""
    bcpStatus = ""
    bcpCapacity = ""
    bcpSerialNum = ""
    bcpPartNumber = ""
    bcpSparePartNumber = ""
    bcpProductVersion = ""

    _properties = (
	dict(id='bcpNumber', type='int',  **_kw),
	dict(id='bcpProductName', type='string',  **_kw),
    dict(id='bcpStatus', type='string', **_kw),
	dict(id='bcpCapacity', type='string',  **_kw),
	dict(id='bcpSerialNum', type='string',  **_kw),
	dict(id='bcpPartNumber', type='string',  **_kw),
	dict(id='bcpSparePartNumber', type='string',  **_kw),
	dict(id='bcpProductVersion', type='string',  **_kw)
    )

    _relations = (
	('bladechassis', ToOne(ToManyCont, 'ZenPacks.community.HPBladeChassis.BladeChassis', 'bladechassispsus')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
	{
	    'id'             : 'BladeChassisPsu',
	    'meta_type'      : 'Blade Chassis Psu',
	    'description'    : 'Blade Chassis Psu Description',
	    'icon'           : 'Device_icon.gif',
	    'product'        : 'BladeServers',
	    'factory'        : 'manage_addBladeServer',
	    'immediate_view' : 'bladeserverPerformance',
	    'actions'        :
	    (
		{ 'id'            : 'perf'
		, 'name'          : 'perf'
		, 'action'        : 'bladeserverPerformance'
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
	return self.bladechassis()

    def managedDeviceLink(self):
	from Products.ZenModel.ZenModelRM import ZenModelRM
	d = self.getDmdRoot("Devices").findDevice(self.bsProductName)
	if d:
	    return ZenModelRM.urlLink(d, 'link')
	return None

    def snmpIgnore(self):
	return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
    

InitializeClass(BladeChassisPsu)
