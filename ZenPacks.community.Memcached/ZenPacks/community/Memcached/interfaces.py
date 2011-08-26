from Products.Zuul.interfaces import IBasicDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IMemcachedDataSourceInfo(IBasicDataSourceInfo):
    component = schema.Text(title=_t(u'Component'))
    eventKey  = schema.Text(title=_t(u'Event Key'))
    timeout   = schema.Int(title=_t(u'Timeout (seconds)'))
    hostname  = schema.Text(title=_t(u'Memcached Host'), readonly=True)
    ipAddress = schema.Text(title=_t(u'Memcached Host IpAddress'), readonly=True)
    parser    = schema.Text(title=_t(u'Parser'), readonly=True)
    port      = schema.Int(title=_t(u'Memcached Port'), required=True)
