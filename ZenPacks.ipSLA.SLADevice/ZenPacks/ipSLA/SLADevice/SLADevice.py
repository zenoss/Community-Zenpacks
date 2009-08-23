from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS
from Products.ZenRelations.RelSchema import *

import copy

class SLADevice(Device):
    "Service Level Agreement Panel"

    _relations = Device._relations + (
        ('ipSLAs', ToManyCont(ToOne, 
            "ZenPacks.ipSLA.SLADevice.SLAS", "host")),
        )
    
    factory_type_information = copy.deepcopy(Device.factory_type_information)
    custom_actions = []
    custom_actions.extend(factory_type_information[0]['actions'])
    custom_actions.insert(2,
           { 'id'            : 'SLADevice'
           , 'name'          : 'Service Level Agreement'
           , 'action'        : 'ipSLAipSlaDevice'
           , 'permissions'   : (ZEN_VIEW,) },
           )
    factory_type_information[0]['actions'] = custom_actions

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()
