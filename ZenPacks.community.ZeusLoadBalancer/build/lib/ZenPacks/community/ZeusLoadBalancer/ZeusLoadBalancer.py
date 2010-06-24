from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenRelations.RelSchema import *

import copy

class ZeusLoadBalancer(Device):
    "Zeus Load Balancer Device"

    _relations = Device._relations + (
    ('pools', ToManyCont(ToOne, "ZenPacks.community.ZeusLoadBalancer.ZeusPool", "zeus")),
    ) + (
    ('virtualServers', ToManyCont(ToOne, "ZenPacks.community.ZeusLoadBalancer.ZeusVirtualServer", "zeus")),
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
        { 'id'            : 'zeusVSDetail'
        , 'name'          : 'Virtual Servers'
        , 'action'        : 'zeusVSDetail'
        , 'permissions'   : (ZEN_VIEW,)
        },
        { 'id'            : 'zeusPoolDetail'
        , 'name'          : 'Pools'
        , 'action'        : 'zeusPoolDetail'
        , 'permissions'   : (ZEN_VIEW,)
        },
        { 'id'            : 'deviceOsDetail'
        , 'name'          : 'OS'
        , 'action'        : 'deviceOsDetail'
        , 'permissions'   : (ZEN_VIEW, )
        },
        { 'id'            : 'deviceHardwareDetail'
        , 'name'          : 'Hardware'
        , 'action'        : 'deviceHardwareDetail'
        , 'permissions'   : (ZEN_VIEW, )
        },
        { 'id'            : 'deviceSoftwareDetail'
        , 'name'          : 'Software'
        , 'action'        : 'deviceSoftwareDetail'
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

InitializeClass(ZeusLoadBalancer)
