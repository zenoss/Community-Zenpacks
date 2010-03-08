from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class PuppetClient(DeviceComponent, ManagedEntity):
    "Puppet Client Information"
    
    portal_type = meta_type = 'PuppetClient'

    pcDisplayName = ""
    pcSigned = -1
    pcState = 1
    pcLastUpdateTime = ""

    _properties = (
	dict(id='pcDisplayName', type='string',  **_kw),
	dict(id='pcSigned', type='int',  **_kw),
	dict(id='pcState', type='int',  **_kw),
	dict(id='pcLastUpdateTime', type='string',  **_kw),
    )

    _relations = (
	('puppetmaster', ToOne(ToManyCont, 'ZenPacks.community.puppet.PuppetMaster', 'puppetclients')),
    )

    factory_type_information = (
	{
	    'id'             : 'PuppetClient',
	    'meta_type'      : 'Puppet Client',
	    'description'    : 'Puppet Client Description',
	    'icon'           : 'Device_icon.gif',
	    'product'        : 'PuppetClients',
	    'factory'        : 'manage_addPuppetClient',
	    'immediate_view' : 'puppetclientDetail',
	    'actions'        :
	    (
		{ 'id'            : 'perf'
		, 'name'          : 'perf'
		, 'action'        : 'puppetclientDetail'
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
	return self.puppetmaster()

    def managedDeviceLink(self):
	from Products.ZenModel.ZenModelRM import ZenModelRM
	d = self.getDmdRoot("Devices").findDevice(self.pcDisplayName)
	if d:
	    return ZenModelRM.urlLink(d, 'link')
	return None

InitializeClass(PuppetClient)

