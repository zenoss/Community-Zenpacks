from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class BladeChassisFan(DeviceComponent, ManagedEntity):
    "Blade Chassis Fan Information"
    
    portal_type = meta_type = 'BladeChassisFan'

    bcfNumber = -1
    bcfProductName = ""
    bcfStatus = ""
    bcfPartNumber = ""
    bcfSparePartNumber = ""
    bcfProductVersion = ""

    _properties = (
	dict(id='bcfNumber', type='int',  **_kw),
	dict(id='bcfProductName', type='string',  **_kw),
	dict(id='bcfStatus', type='string',  **_kw),
	dict(id='bcfPartNumber', type='string',  **_kw),
	dict(id='bcfSparePartNumber', type='string',  **_kw),
	dict(id='bcfProductVersion', type='string',	**_kw)
    )

    _relations = (
	('bladechassis', ToOne(ToManyCont, 'ZenPacks.community.HPBladeChassis.BladeChassis', 'bladechassisfans')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
	{
	    'id'             : 'BladeChassisFan',
	    'meta_type'      : 'Blade Chassis Fan',
	    'description'    : 'Blade Chassis Fan Description',
	    'icon'           : 'Device_icon.gif',
	    'product'        : 'BladeChassisFans',
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
	d = self.getDmdRoot("Devices").findDevice(self.bcfProductName)
	if d:
	    return ZenModelRM.urlLink(d, 'link')
	return None

    def snmpIgnore(self):
	return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
    

InitializeClass(BladeChassisFan)
