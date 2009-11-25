######################################################################
#
# Pdu7930 object class
#
######################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class Pdu7930(Device):
    "A PDU Device"

    _relations = Device._relations + (
        ('PduOutlet7930', ToManyCont(ToOne,
            'ZenPacks.Iwillfearnoevil.Powernet7930.PduOutlet7930', 'Pdu7930')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)
    factory_type_information[0]['actions'] += (
            { 'id'              : 'Outlet7930'
            , 'name'            : 'PDU Outlets'
            , 'action'          : 'Pdu7930Detail'
            , 'permissions'     : (ZEN_VIEW, ) },
            )


    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(Pdu7930)

