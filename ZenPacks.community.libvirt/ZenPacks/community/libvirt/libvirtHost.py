from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenRelations.RelSchema import *

import copy

class libvirtHost(Device):
    "libvirt Host Device"

    _relations = Device._relations + (
	('libvirtguests', ToManyCont(ToOne, "ZenPacks.community.libvirt.libvirtGuest", "libvirthost")),
	('libvirtpools', ToManyCont(ToOne, "ZenPacks.community.libvirt.libvirtPool", "libvirtpool")),
	('libvirtvolumes', ToManyCont(ToOne, "ZenPacks.community.libvirt.libvirtVolume", "libvirtvolume")),
    )
    
    factory_type_information = (
	{
	    'immediate_view' : 'deviceStatus',
	    'actions'        : (
		{ 'id'            : 'status'
		, 'name'          : 'Status'
		, 'action'        : 'deviceStatus'
		, 'permissions'   : (ZEN_VIEW, )
		},
		{ 'id'            : 'osdetail'
		, 'name'          : 'OS'
		, 'action'        : 'deviceOsDetail'
		, 'permissions'   : (ZEN_VIEW, )
		},
		{ 'id'            : 'libvirtguestData'
		, 'name'          : 'Guests'
		, 'action'        : 'libvirtguestData'
		, 'permissions'   : (ZEN_VIEW,)
		},
		{ 'id'            : 'libvirtpoolData'
		, 'name'          : 'Pools'
		, 'action'        : 'libvirtpoolData'
		, 'permissions'   : (ZEN_VIEW,)
		},
		{ 'id'            : 'libvirtvolumeData'
		, 'name'          : 'Volumes'
		, 'action'        : 'libvirtvolumeData'
		, 'permissions'   : (ZEN_VIEW,)
		},
		{ 'id'            : 'hwdetail'
		, 'name'          : 'Hardware'
		, 'action'        : 'deviceHardwareDetail'
		, 'permissions'   : (ZEN_VIEW, )
		},
		{ 'id'            : 'events'
		, 'name'          : 'Events'
		, 'action'        : 'viewEvents'
		, 'permissions'   : (ZEN_VIEW, )
		},
		{ 'id'            : 'perfServer'
		, 'name'          : 'Perf'
		, 'action'        : 'viewDevicePerformance'
		, 'permissions'   : (ZEN_VIEW, )
		},
		{ 'id'            : 'edit'
		, 'name'          : 'Edit'
		, 'action'        : 'editDevice'
		, 'permissions'   : ("Change Device",)
		},
	    )
	},
    )

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()

    def getVirtHostType(self):
	typemap = ['qemu','xen','openvz','esx','opennebula','lxc','vbox','uml']
	type = 'unknown'
	for t in typemap:
	    if self.zLibvirtConnectType.startswith(t):
		type = t
	if type == 'qemu':
	    type = 'qemu/kvm'
	return type

InitializeClass(libvirtHost)
