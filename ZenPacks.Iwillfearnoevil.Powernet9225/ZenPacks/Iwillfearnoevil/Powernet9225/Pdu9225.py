######################################################################
#
# Pdu9225 object class
#
######################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class Pdu9225(Device):
    "A PDU Device"

    _relations = Device._relations + (
        ('PduOutlet', ToManyCont(ToOne,
            'ZenPacks.speakeasy.Powernet9225.PduOutlet', 'Pdu9225')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)
    factory_type_information[0]['actions'] += (
            { 'id'              : 'PduOutlet'
            , 'name'            : 'PDU Outlets'
            , 'action'          : 'Pdu9225Detail'
            , 'permissions'     : (ZEN_VIEW, ) },
            )


    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(Pdu9225)
