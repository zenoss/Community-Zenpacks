from Products.Zuul.infos import ProxyProperty
from zope.interface import implements
from Products.Zuul.infos.template import BasicDataSourceInfo
from ZenPacks.community.Memcached.interfaces import IMemcachedDataSourceInfo
	
	
class MemcachedDataSourceInfo(BasicDataSourceInfo):
    implements(IMemcachedDataSourceInfo)
    component = ProxyProperty('component')
    eventKey  = ProxyProperty('eventKey')
    timeout   = ProxyProperty('timeout')
    hostname  = ProxyProperty('hostname')
    ipAddress = ProxyProperty('ipAddress')
    port      = ProxyProperty('port')
    parser    = ProxyProperty('parser')
    @property
    def testable(self):
        """We can NOT test this datsource against a specific device
        """
	return False
