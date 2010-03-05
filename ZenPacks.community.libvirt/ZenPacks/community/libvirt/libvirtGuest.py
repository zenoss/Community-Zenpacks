from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class libvirtGuest(DeviceComponent, ManagedEntity):
    "libvirt Guest Information"
    
    portal_type = meta_type = 'libvirtGuest'

    lvDisplayName = ""
    lvMaxMemory = -1
    lvNumberVirtCPUs = -1
    lvOSType = ""
    lvUUIDString = ""
    lvState = -1

    _properties = (
	dict(id='lvDisplayName', type='string',  **_kw),
	dict(id='lvState', type='int',  **_kw),
	dict(id='lvMaxMemory', type='int',  **_kw),
	dict(id='lvNumberVirtCPUs', type='int',  **_kw),
	dict(id='lvOSType',	type='string',  **_kw),
	dict(id='lvUUIDString',	type='string',  **_kw),
    )

    _relations = (
	('libvirthost', ToOne(ToManyCont, 'ZenPacks.community.libvirt.libvirtHost', 'libvirtguests')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
	{
	    'id'             : 'libvirtGuest',
	    'meta_type'      : 'libvirt Guest',
	    'description'    : 'libvirt Guest Description',
	    'icon'           : 'Device_icon.gif',
	    'product'        : 'libvirtGuests',
	    'factory'        : 'manage_addlibvirtGuest',
	    'immediate_view' : 'libvirtguestPerformance',
	    'actions'        :
	    (
		{ 'id'            : 'perf'
		, 'name'          : 'perf'
		, 'action'        : 'libvirtguestPerformance'
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
	return self.libvirthost()

    def managedDeviceLink(self):
	from Products.ZenModel.ZenModelRM import ZenModelRM
	d = self.getDmdRoot("Devices").findDevice(self.lvDisplayName)
	if d:
	    return ZenModelRM.urlLink(d, 'link')
	return None

    def getStateString(self):
        statestrmap = ['NoState', 'Running', 'Blocked', 'Paused', 'Shutdown', 'Shutoff', 'Crashed']
        state = self.getRRDValue('state')
        if state == None:
	    state = self.lvState
	if state == None or state == '':
	    return "Unknown"
        return statestrmap[int(state)]

InitializeClass(libvirtGuest)
