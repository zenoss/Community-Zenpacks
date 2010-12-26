################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of modules.

$Id: info.py,v 1.1 2010/12/14 21:57:58 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import ThresholdInfo
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.community.CiscoEnvMon import interfaces


class CiscoExpansionCardInfo(ComponentInfo):
    implements(interfaces.ICiscoExpansionCardInfo)

    serialNumber = ProxyProperty("serialNumber")
    slot = ProxyProperty("slot")
    HWVer = ProxyProperty("HWVer")
    SWVer = ProxyProperty("SWVer")
    FWRev = ProxyProperty("FWRev")

    @property
    def partNumber(self):
        self._object.getProductPartNumber()

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    def status(self):
        if hasattr(self._object, 'statusString'):
            return self._object.statusString()
        elif hasattr(self._object, 'state'):
            return self._object.state
        else: return 'Unknown'


class CiscoFanInfo(ComponentInfo):
    implements(interfaces.ICiscoFanInfo)

    @property
    def rpmString(self):
        return self._object.rpmString()

    @property
    def status(self):
        if hasattr(self._object, 'statusString'):
            return self._object.statusString()
        elif hasattr(self._object, 'state'):
            return self._object.state
        else: return 'Unknown'


class CiscoTemperatureSensorInfo(ComponentInfo):
    implements(interfaces.ICiscoTemperatureSensorInfo)

    @property
    def tempString(self):
        tc = self._object.temperatureCelsiusString()
        tf = self._object.temperatureFahrenheitString()
        if tc == tf: return tc
        return tc + " / " + tf

    @property
    def status(self):
        if hasattr(self._object, 'statusString'):
            return self._object.statusString()
        elif hasattr(self._object, 'state'):
            return self._object.state
        else: return 'Unknown'


class CiscoPowerSupplyInfo(ComponentInfo):
    implements(interfaces.ICiscoPowerSupplyInfo)

    type = ProxyProperty("type")

    @property
    def wattsString(self):
        return self._object.wattsString()

    @property
    def millivoltsString(self):
        return self._object.millivoltsString()

    @property
    def status(self):
        if hasattr(self._object, 'statusString'):
            return self._object.statusString()
        elif hasattr(self._object, 'state'):
            return self._object.state
        else: return 'Unknown'

