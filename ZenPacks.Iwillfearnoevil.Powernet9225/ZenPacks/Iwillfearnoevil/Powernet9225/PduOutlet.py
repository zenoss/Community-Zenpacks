######################################################################
#
# PduOutlet object class
#
######################################################################

__doc__="""PduOutlet

PduOutlet is a component of Pdu9225

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity


class PduOutlet(DeviceComponent, ManagedEntity):
    """Pdu Outlet object"""

    event_key = portal_type = meta_type = 'PduOutlet'
    
    #**************Custom data Variables here from modeling************************
    
    OutletController = 'pdu1a-1'
    OutletNumber = '1'
    DeviceControlled = 'xs1a'
    State = '1'
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'OutletController', 'type':'string', 'mode':''},
        {'id':'OutletNumber', 'type':'string', 'mode':''},
        {'id':'DeviceControlled', 'type':'string', 'mode':''},
        {'id':'State', 'type':'int', 'mode':''}
        )
    #****************
    
    _relations = (
        ("Pdu9225", ToOne(ToManyCont,
            "ZenPacks.speakeasy.Powernet9225.Pdu9225", "PduOutlet")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'PduOutlet',
            'meta_type'      : 'PduOutlet',
            'description'    : """PDU Outlet info""",
            'product'        : 'Powernet9225',
            'immediate_view' : 'viewPduOutlet',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'PDU Outlet Status'
                , 'action'        : 'viewPduOutlet'
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
	if self.OutletController == 'Undefined' \
	    or self.OutletNumber == '0':
		return "Unknown"
	else:
                return str( self.OutletNumber ) + " Outlet " + self.OutletController

#    name = primarySortKey = viewName
    name = viewName

    def primarySortKey(self):
        """sort on PDU Number"""
        return self.OutletController

    def device(self):
        return self.Pdu9225()

#   def OutletController(self):
#        return self.OutletController()

#   def State(self):
#        return self.State()

#   def OutletNumber(self):
#        return self.OutletNumber()

#   def DeviceControlled(self):
#        return self.DeviceControlled()
    
#    def getOutletController(self):
#        dmd=self.dmd
#        devmac=self.RemoteAddress
#        IpAddress=[]
#        Ips=dmd.ZenLinkManager.layer2_catalog(macaddress=devmac)
#        for i in Ips:
#            IpAddress=IpAddress + [i.getObject().manageIp]
#        return IpAddress

#    def getIpRemoteIfDesc(self):
#        dmd=self.dmd
#        devmac=str(self.RemoteAddress)
#        IfDesc=[]
#        Ips=dmd.ZenLinkManager.layer2_catalog(macaddress=devmac)
#        for i in Ips:
#            IfDesc=IfDesc + [i.getObject().id]
#        return IfDesc
        
#    def getIpRemoteHostname(self):
#        dmd=self.dmd
#        find = dmd.Devices.findDevice
#        devmac=str(self.RemoteAddress)
#        Hostname=[]
#        Ips=dmd.ZenLinkManager.layer2_catalog(macaddress=devmac)
#        for i in Ips:
#            Hostname=Hostname + [find(i.getObject().manageIp).id]
#        return Hostname
#         OutletController=OutletController + [i.getObject().OutletController]        
    	
    #THIS FUNCTION IS REQUIRED LEAVE IT BE IF NO RRD INFO IS PRESENT	    
    def getRRDNames(self):
	return []


InitializeClass(PduOutlet)
