######################################################################
#
# CfengineDevice object class
#
######################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW

import copy

class CfengineDevice(Device):
    "A Cfengine Device"

    _relations = Device._relations + (
	('cfengineclients', ToManyCont(ToOne, "ZenPacks.community.Cfengine.CfengineClient", "cfengineserver")),
    )

    factory_type_information = (
        {
            'immediate_view' : 'deviceStatus',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'deviceStatus'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'cfengineclientData'
                , 'name'          : 'Clients'
                , 'action'        : 'cfengineClientData'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'osdetail'
                , 'name'          : 'OS'
                , 'action'        : 'deviceOsDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'hwdetail'
                , 'name'          : 'Hardware'
                , 'action'        : 'deviceHardwareDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'swdetail'
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

InitializeClass(CfengineDevice)
