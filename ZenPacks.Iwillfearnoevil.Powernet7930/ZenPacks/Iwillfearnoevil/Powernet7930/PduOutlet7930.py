######################################################################
#
# PduOutlet7930 object class
#
######################################################################

__doc__="""PduOutlet7930

PduOutlet7930 is a component of Pdu7930

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity


class PduOutlet7930(DeviceComponent, ManagedEntity):
    """Pdu Outlet object"""

    event_key = portal_type = meta_type = 'PduOutlet7930'
    
    #**************Custom data Variables here from modeling************************
    
    OutletNumber = '1'
    DeviceControlled = 'xs1a'
    Status = '1'
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'OutletNumber', 'type':'int', 'mode':''},
        {'id':'DeviceControlled', 'type':'string', 'mode':''},
        {'id':'Status', 'int':'string', 'mode':''}
        )
    #****************
    
    _relations = (
        ("Pdu7930", ToOne(ToManyCont,
            "ZenPacks.Iwillfearnoevil.Powernet7930.Pdu7930", "PduOutlet7930")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'PduOutlet7930',
            'meta_type'      : 'PduOutlet7930',
            'description'    : """PDU Outlet info""",
            'product'        : 'Powernet7930',
            'immediate_view' : 'viewPduOutlet',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'PDU Outlet Status'
                , 'action'        : 'viewPduOutlet7930'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Pdu Outlet Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                },                
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW, )
                },
            )
          },
        ) 


    def viewName(self):
        if self.DeviceControlled == 'Undefined' \
            or self.OutletNumber == '0':
                return "Unknown"
        else:
             	return str( self.OutletNumber ) + " Outlet " + self.DeviceControlled

#    name = primarySortKey = viewName
    name = viewName


    def primarySortKey(self):
        """sort on PDU Number"""
        return self.OutletNumber

    def device(self):
        return self.Pdu7930()


#    def viewName(self):
#	if self.OutletController == 'Undefined' \
#	    or self.OutletNumber == '0':
#		return "Unknown"
#	else:
#                return str( self.OutletNumber ) + " Outlet " + self.OutletController

#    def StateArray(self):
#        State01 = self.OutletState.strip().split('  ')
#        return State01[(self.OutletNumber -1)]

    #THIS FUNCTION IS REQUIRED LEAVE IT BE IF NO RRD INFO IS PRESENT
    def getRRDNames(self):
        return []

InitializeClass(PduOutlet7930)
