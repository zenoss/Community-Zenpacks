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

import logging
log = logging.getLogger('BridgeInterface')

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
        """Pretty version human readable version of this object"""
        if self.RemoteAddress == '00:00:00:00:00:00' or self.Port == '-1':
            return "Unknown"
        else:
            return str( self.Port ) + " - " + self.RemoteAddress


    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName

    def primarySortKey(self):
        """Sort by port number then remote MAC"""
        return "%s%s" % (self.Port, self.RemoteAddress)

    def device(self):
        return self.BridgeDev()
    
    def monitored(self):
        """
        If a bridge channel exists start monitoring it. Because channels are
        very dynamic we will just assume that they should be modeled if they
        exist. Of cuorse the modeler would need to run very fequently to give
        accurate results as to who is talking at any given time. Looks like
        the default timeout on a cisco switch is 5 minutes so the modeler
        would need to run at about that frequency to keep this table accurate.
        If you increase the timeout you will get more accurate resuslts with a
        longer modeling cycle. The max time on a cisco box is 12 hours.
        """
        return True
        
    def getRemoteInterfaces(self):
        """
        return html snipits used in the UI to display links to remote
        interfaces for a MAC and their associated IP addresses.
        """
        interfaces = []
        for intobj in self._getInterfaces():
            ipaddrs = [ip.urlLink() for ip in intobj.getIpAddressObjs()]
            interfaces.append('<p style="padding:0.5em">%s: %s</p>' %
                            (intobj.urlLink(), ", ".join(ipaddrs)))
        return interfaces

    def getRemoteDevice(self):
        """
        return the remote device object for this bridge port. If any are
        returned based on the MAC query we take the first one assuming that
        MACs are unique to devices (eventhough they aren't on interfaces)
        """
        intobj = self._getInterfaces()
        if len(intobj) > 0 and intobj[0].device(): 
            return intobj[0].device().urlLink()

    def _getInterfaces(self):
        """
        return a list of interfaces that match a MAC address from the layer2
        index. There can be many interfaces per MAC because logical interfaces
        on one physical port share the same MAC.
        """
        intobjs = []
        for brain in self.dmd.ZenLinkManager.layer2_catalog(
                        macaddress=self.RemoteAddress):
            try:
                intobj = brain.getObject()
                intobjs.append(intobj)
            except KeyError, e:
                log.error('object %s not found from layer2 index'
                            'the index needs to be rebuilt')
        return intobjs
        
    #THIS FUNCTION IS REQUIRED LEAVE IT BE IF NO RRD INFO IS PRESENT
    # I don't really understand this -EAD
    def getRRDNames(self):
        return []


InitializeClass(BridgeInterface)
