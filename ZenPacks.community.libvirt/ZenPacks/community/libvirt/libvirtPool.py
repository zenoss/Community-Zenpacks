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

class libvirtPool(DeviceComponent, ManagedEntity):
    "libvirt Pool Information"
    
    portal_type = meta_type = 'libvirtPool'

    lvDisplayName = ""
    lvUUIDString = ""
    lvState = -1
    lvCapacity = -1
    lvVolumes = []

    _properties = (
	dict(id='lvDisplayName', type='string',  **_kw),
	dict(id='lvUUIDString',	type='string',  **_kw),
	dict(id='lvState', type='int',  **_kw),
	dict(id='lvCapacity', type='int',  **_kw),
	dict(id='lvVolumes',	type='lines',  **_kw), # The list of volume keys
    )

    _relations = (
	('libvirthost', ToOne(ToManyCont, 'ZenPacks.community.libvirt.libvirtHost', 'libvirtpools')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
	{
	    'id'             : 'libvirtPool',
	    'meta_type'      : 'libvirt Pool',
	    'description'    : 'libvirt Pool Description',
	    'icon'           : 'Device_icon.gif',
	    'product'        : 'libvirtPools',
	    'factory'        : 'manage_addlibvirtPool',
	    'immediate_view' : 'libvirtpoolPerformance',
	    'actions'        :
	    (
		{ 'id'            : 'perf'
		, 'name'          : 'perf'
		, 'action'        : 'libvirtpoolPerformance'
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

    def getStateString(self):
        statestrmap = ['Inactive','Building','Running','Degraded']
        state = self.getRRDValue('state')
        if state == None:
	    state = self.lvState
	if state == None or state == '':
	    return "Unknown"
        return statestrmap[int(state)]

    def dolibvirtStart(self):
	self.dolibvirtCommand('pool-start')

    def dolibvirtDestroy(self):
	self.dolibvirtCommand('pool-destroy')

    def dolibvirtCommand(self,libvirtcommand):
	libvirtpath = self.pack().path()
	command = os.path.join(libvirtpath,'libexec','check_libvirt.py')
        args = ' -H ' + self.libvirthost().id + ' -c ' + self.zLibvirtConnectType + ' -u ' + self.zLibvirtUsername + ' -l ' + libvirtcommand + ' -n ' + self.lvDisplayName
        if self.zLibvirtPassword != '' and self.zLibvirtConnectType == 'esx://':
            args += ' -p ' + self.zLibvirtPassword
        output = Popen(command + args, stdout=PIPE, shell=True, env={"PATH": "/usr/bin"}).communicate()[0] # have to reset the environment or zenoss overrides python values....
	return output

InitializeClass(libvirtPool)

