######################################################################
#
# BridgeInterface object class
#
######################################################################

__doc__="""BridgeInt

BridgeInt is a component of a Bridge Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity


class BridgeInterface(DeviceComponent, ManagedEntity):
    """Bridge Interface object"""

    event_key = portal_type = meta_type = 'BridgeInterface'
    
    #**************Custom data Variables here from modeling************************
    
    RemoteAddress = '00:00:00:00:00:00'
    Port = '-1'
    PortIfIndex = 2
    PortStatus = '4'
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'RemoteAddress', 'type':'string', 'mode':''},
        {'id':'Port', 'type':'string', 'mode':''},
        {'id':'PortIfIndex', 'type':'int', 'mode':''},
        {'id':'PortStatus', 'type':'string', 'mode':''}
        )
    #****************
    
    _relations = (
        ("BridgeDev", ToOne(ToManyCont,
            "ZenPacks.skills1st.bridge.BridgeDevice", "BridgeInt")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'BridgeInterface',
            'meta_type'      : 'BridgeInterface',
            'description'    : """Bridge Interface info""",
            'product'        : 'bridge',
            'immediate_view' : 'viewBridgeInterface',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Bridge Interface Status'
                , 'action'        : 'viewBridgeInterface'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Bridge Interface Template'
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
	if self.RemoteAddress == '00:00:00:00:00:00' \
	    or self.Port == '-1':
		return "Unknown"
	else:
                return str( self.Port ) + "/" + self.RemoteAddress

#    name = primarySortKey = viewName
    name = viewName

    def primarySortKey(self):
        """sort on Port status"""
        return self.PortStatus

    def device(self):
        return self.BridgeDev()
    
    def getIpRemoteAddress(self):
        dmd=self.dmd
        devmac=self.RemoteAddress
        IpAddress=[]
        Ips=dmd.ZenLinkManager.layer2_catalog(macaddress=devmac)
        for i in Ips:
            IpAddress=IpAddress + [i.getObject().manageIp]
        return IpAddress

    def getIpRemoteIfDesc(self):
        dmd=self.dmd
        devmac=str(self.RemoteAddress)
        IfDesc=[]
        Ips=dmd.ZenLinkManager.layer2_catalog(macaddress=devmac)
        for i in Ips:
            IfDesc=IfDesc + [i.getObject().id]
        return IfDesc
        
    def getIpRemoteHostname(self):
        dmd=self.dmd
        find = dmd.Devices.findDevice
        devmac=str(self.RemoteAddress)
        Hostname=[]
        Ips=dmd.ZenLinkManager.layer2_catalog(macaddress=devmac)
        for i in Ips:
            Hostname=Hostname + [find(i.getObject().manageIp).id]
        return Hostname
        
    	
    #THIS FUNCTION IS REQUIRED LEAVE IT BE IF NO RRD INFO IS PRESENT	    
    def getRRDNames(self):
	return []


InitializeClass(BridgeInterface)
