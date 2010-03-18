from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

# for external sets...
from subprocess import *
import os

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
    lvVolumes = []

    _properties = (
	dict(id='lvDisplayName', type='string',  **_kw),
	dict(id='lvState', type='int',  **_kw),
	dict(id='lvMaxMemory', type='int',  **_kw),
	dict(id='lvNumberVirtCPUs', type='int',  **_kw),
	dict(id='lvOSType',	type='string',  **_kw),
	dict(id='lvUUIDString',	type='string',  **_kw),
	dict(id='lvVolumes',	type='lines',  **_kw), # The list of volume names (which are stored under the host)
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

    def dolibvirtSave(self):
	self.dolibvirtCommand('save')

    def dolibvirtResume(self):
	self.dolibvirtCommand('resume')

    def dolibvirtStartup(self):
	self.dolibvirtCommand('startup')

    def dolibvirtShutdown(self):
	self.dolibvirtCommand('shutdown')

    def dolibvirtDestroy(self):
	self.dolibvirtCommand('destroy')


    def dolibvirtCommand(self,libvirtcommand):
	libvirtpath = self.pack().path()
	command = os.path.join(libvirtpath,'libexec','check_libvirt.py')
        args = ' -H ' + self.libvirthost().id + ' -c ' + self.zLibvirtConnectType + ' -u ' + self.zLibvirtUsername + ' -l ' + libvirtcommand + ' -n ' + self.lvDisplayName
        if self.zLibvirtPassword != '' and self.zLibvirtConnectType == 'esx://':
            args += ' -p ' + self.zLibvirtPassword
        output = Popen(command + args, stdout=PIPE, shell=True, env={"PATH": "/usr/bin"}).communicate()[0] # have to reset the environment or zenoss overrides python values....
	return output

InitializeClass(libvirtGuest)

