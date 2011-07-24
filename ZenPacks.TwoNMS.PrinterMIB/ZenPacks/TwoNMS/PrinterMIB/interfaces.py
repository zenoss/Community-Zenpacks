from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IPrinterMIBInfo(IComponentInfo):
    """
Info adapter for PrinterMIB Supply component
"""
    Color = schema.Text(title=u"Color", readonly=True, group='Details')
    Description = schema.Text(title=u"Supply Description", readonly=True, group='Details')
    MaxLevel = schema.Text(title=u"Maximum Level", readonly=True, group='Details')
    CurrentLevel = schema.Text(title=u"Current Level", readonly=True, group='Details')
    SupplyType = schema.Text(title=u"Supply Type", readonly=True, group='Details')
    SupplyTypeUnit = schema.Text(title=u"Supply Type Measurement Unit", readonly=True, group='Details')
    rgbColorCode = schema.Text(title=u"RGB Color Code", readonly=False, group='Details')


