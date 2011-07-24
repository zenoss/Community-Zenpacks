__doc__="""info.py

Representation PrinterMIB Supply

$Id: info.py,v 1.2 2010/12/14 20:45:46 jc Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
#from Products.ZenUtils.Utils import convToUnits
from ZenPacks.TwoNMS.PrinterMIB import interfaces


class PrinterMIBInfo(ComponentInfo):
    implements(interfaces.IPrinterMIBInfo)

    Description = ProxyProperty("prtMarkerSuppliesDescription")
    Color = ProxyProperty("prtMarkerColorantValue")
    MaxLevel = ProxyProperty("prtMarkerSuppliesMaxCapacity")
    CurrentLevel = ProxyProperty("prtMarkerSuppliesLevel")
    rgbColorCode = ProxyProperty("rgbColorCode")
    SupplyType = ProxyProperty("PrtMarkerSuppliesTypeTC")
    SupplyTypeUnit = ProxyProperty("PrtMarkerSuppliesSupplyUnitTC")

