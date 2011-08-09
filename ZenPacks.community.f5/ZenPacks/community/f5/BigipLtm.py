"""
BigIP LTM Device
"""

import Globals
from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenRelations.RelSchema import *
from copy import deepcopy


class BigipLtm(Device):
    """
    A class to represent a physical LTM
    """
    
    sysProductBuild = ""
    sysProductVersion = ""
    sysProductEdition = ""
    sysProductName = ""
    
    #_relations = Device._relations
    _relations = Device._relations + (
        ('LtmVs', ToManyCont(ToOne,
                        'ZenPacks.community.f5.BigipVirtualServer', 'Ltm')),
    )
    _properties = (
        {'id': 'sysProductBuild', 'type': 'string', 'mode': ''},
        {'id': 'sysProductVersion', 'type': 'string', 'mode': ''},
        {'id': 'sysProductEdition', 'type': 'string', 'mode': ''},
        {'id': 'sysProductName', 'type': 'string', 'mode': ''},
    )

   
    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()
        
InitializeClass(BigipLtm)