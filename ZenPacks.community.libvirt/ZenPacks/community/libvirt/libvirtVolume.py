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

class libvirtVolume(DeviceComponent, ManagedEntity):
    "libvirt Volume Information"
    
    portal_type = meta_type = 'libvirtVolume'

    lvDisplayName = ""
    lvPath = ""
    lvKey = "" # Unique ID ... usually the same as the path... can be looked up with this without the pool name...
    lvType = -1
    lvCapacity = -1
    lvPool = "" # the display name is only unique within a pool.

    _properties = (
	dict(id='lvDisplayName', type='string',  **_kw),
	dict(id='lvPath',	type='string',  **_kw),
	dict(id='lvKey',	type='string',  **_kw),
	dict(id='lvType', type='int',  **_kw),
	dict(id='lvCapacity', type='int',  **_kw),
	dict(id='lvPool',	type='string',  **_kw), # the pool this belongs to
    )

    _relations = (
	('libvirthost', ToOne(ToManyCont, 'ZenPacks.community.libvirt.libvirtHost', 'libvirtvolumes')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
	{
	    'id'             : 'libvirtVolume',
	    'meta_type'      : 'libvirt Volume',
	    'description'    : 'libvirt Volume Description',
	    'icon'           : 'Device_icon.gif',
	    'product'        : 'libvirtVolumes',
	    'factory'        : 'manage_addlibvirtVolume',
	    'immediate_view' : 'libvirtvolumePerformance',
	    'actions'        :
	    (
		{ 'id'            : 'perf'
		, 'name'          : 'perf'
		, 'action'        : 'libvirtvolumePerformance'
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

    def dolibvirtDelete(self):
	self.dolibvirtCommand('vol-delete')

    def dolibvirtCommand(self,libvirtcommand):
	libvirtpath = self.pack().path()
	command = os.path.join(libvirtpath,'libexec','check_libvirt.py')
        args = ' -H ' + self.libvirthost().id + ' -c ' + self.zLibvirtConnectType + ' -u ' + self.zLibvirtUsername + ' -l ' + libvirtcommand + ' -n ' + self.lvDisplayName
        if self.zLibvirtPassword != '' and self.zLibvirtConnectType == 'esx://':
            args += ' -p ' + self.zLibvirtPassword
        output = Popen(command + args, stdout=PIPE, shell=True, env={"PATH": "/usr/bin"}).communicate()[0] # have to reset the environment or zenoss overrides python values....
	return output

InitializeClass(libvirtVolume)

