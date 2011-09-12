"""
"""

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IBigipVirtualServerInfo(IComponentInfo):
    """
    Info adapter for BigipVirtualServer components.
    """
    vsIP = schema.Text(title=u"IP Address", readonly=True, group='Details')
    ltmVirtualServPort = schema.Text(title=u"Port", readonly=True, group='Details')
    VsStatusAvailState = schema.Text(title=u"Availability Status", readonly=True, group='Details')
    VsStatusEnabledState = schema.Text(title=u"Enabled/Disabled", readonly=True, group='Details')
    VsStatusDetailReason = schema.Text(title=u"Status Details", readonly=True, group='Details')
