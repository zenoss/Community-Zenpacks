from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class CfengineClient(DeviceComponent, ManagedEntity):
    "Cfengine Client Information"
    
    portal_type = meta_type = 'CfengineClient'

    cfcDisplayName = ""
    cfcCompliance = 0

    _properties = (
	dict(id='cfcDisplayName', type='string',  **_kw),
	dict(id='cfcCompliance', type='int',  **_kw),
    )

    _relations = (
	('cfengineserver', ToOne(ToManyCont, 'ZenPacks.community.Cfengine.CfengineDevice', 'cfengineclients')),
    )

    factory_type_information = (
	{
	    'id'             : 'CfengineClient',
	    'meta_type'      : 'Cfengine Client',
	    'description'    : 'Cfengine Client Description',
	    'icon'           : 'Device_icon.gif',
	    'product'        : 'CfengineClients',
	    'factory'        : 'manage_addCfengineClient',
	    'immediate_view' : 'cfengineclientDetail',
	    'actions'        :
	    (
		{ 'id'            : 'perf'
		, 'name'          : 'perf'
		, 'action'        : 'cfengineclientDetail'
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
	return self.cfengineserver()

    def managedDeviceLink(self):
	from Products.ZenModel.ZenModelRM import ZenModelRM
	d = self.getDmdRoot("Devices").findDevice(self.cfcDisplayName)
	if d:
	    return ZenModelRM.urlLink(d, 'link')
	return None

InitializeClass(CfengineClient)

