"""
BigIP LTM Device
"""

import Globals
from Globals import InitializeClass
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy

class BigipVirtualServer(DeviceComponent, ManagedEntity):
    """
    A class to represent a virtual server running on an LTM
    """
   
    portal_type = meta_type = "BigipVirtualServer"
    
    ltmVirtualServName = "DefaultVirtualServer"
    vsIP = "000.000.000.000"
    ltmVirtualServPort = 0
    VsStatusAvailState = None
    VsStatusEnabledState = None
    VsStatusDetailReason = None
    status = ""
    _properties = (
        {'id': 'ltmVirtualServName', 'type': 'string', 'mode': ''},
        {'id': 'vsIP', 'type': 'string', 'mode': ''},
        {'id': 'ltmVirtualServPort', 'type': 'integer', 'mode': ''},
    )

    _relations = (
        ('Ltm', ToOne(ToManyCont,'ZenPacks.community.f5.BigipLtm', 'LtmVs')),
    )

    factory_type_information = (
    {
        'id': 'BigipVirtualServer',
        'meta_type': 'BigipVirtualServer',
        'description': 'Virtual Server Information',
        'product': 'f5',
        'immediate_view' : 'graphs',
        'actions'        : (
           # This populates the Dropdown box when viewing virtual servers.
           # Via some magic I don't yet understand, events and details are
           # In the menu without interaction. However The following is needed
           # to add graphs as a menu option. This leverages a native skin
           # And we don't need to provide our own.
           # { 'id'            : 'graphs'
           # , 'name'          : 'Graphs'
           # , 'action'        : 'graphs'
           # , 'permissions'   : (ZEN_VIEW, )
           # },
            # Lets also enable modification history, just cause we can
            # Again this is a default skin, and not one this pack is providing.
            { 'id'            : 'viewHistory'
            , 'name'          : 'Modifications'
            , 'action'        : 'viewHistory'
            , 'permissions'   : (ZEN_VIEW, )
            },
        )
    },
    )

    def device(self):
        return self.Ltm()
    
    def monitored(self):
        """
        If a virtual server exists, we want to default to monitoring it.
        """ 
        return True
    
    #def __init__(self, *args, **kw):
    #    Device.__init__(self, *args, **kw)
    #    self.buildRelations()
        
InitializeClass(BigipVirtualServer)