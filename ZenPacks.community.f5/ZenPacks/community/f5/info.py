"""
"""

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
#from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.f5 import interfaces

class BigipVirtualServerInfo(ComponentInfo):
    implements(interfaces.IBigipVirtualServerInfo)
    
    vsIP = ProxyProperty("vsIP")
    ltmVirtualServPort = ProxyProperty("ltmVirtualServPort")
    VsStatusAvailState = ProxyProperty("VsStatusAvailState")
    VsStatusEnabledState = ProxyProperty("VsStatusEnabledState")
    VsStatusDetailReason = ProxyProperty("VsStatusDetailReason")
    # I am not exactly sure why I need this status entry here
    # However without it, the status in the component grid always 
    # showed as Up, adding this, seems to make it honor the status
    # I set in the modeler
    status = ProxyProperty("status")
    
    #@property
    #def ip_address(self):
    #    return self._object.get_ip_address()