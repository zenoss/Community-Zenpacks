################################################################################
#
# This program is part of the deviceAdvDetail Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of Data Source.

$Id: info.py,v 1.0 2010/06/24 12:32:04 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import ThresholdInfo
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.community.deviceAdvDetail import interfaces


class StatusThresholdInfo(ThresholdInfo):
    implements(interfaces.IStatusThresholdInfo)
    eventClass = ProxyProperty("eventClass")
    escalateCount = ProxyProperty("escalateCount")

class MemoryModuleInfo(ComponentInfo):
    implements(interfaces.IMemoryModuleInfo)

    size = ProxyProperty("size")

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
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class LogicalDiskInfo(ComponentInfo):
    implements(interfaces.ILogicalDiskInfo)

    description = ProxyProperty("description")
    diskType = ProxyProperty("diskType")
    size = ProxyProperty("size")
    stripesize = ProxyProperty("stripesize")

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class ExpansionCardInfo(ComponentInfo):
    implements(interfaces.IExpansionCardInfo)

    serialNumber = ProxyProperty("serialNumber")
    slot = ProxyProperty("slot")

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
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class HardDiskInfo(ComponentInfo):
    implements(interfaces.IHardDiskInfo)

    serialNumber = ProxyProperty("serialNumber")
    diskType = ProxyProperty("diskType")
    size = ProxyProperty("size")
    FWRev = ProxyProperty("FWRev")
    rpm = ProxyProperty("rpm")
    bay = ProxyProperty("bay")

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
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class FanInfo(ComponentInfo):
    implements(interfaces.IFanInfo)
    
    @property
    def rpmString(self):
        return self._object.rpmString()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class TemperatureSensorInfo(ComponentInfo):
    implements(interfaces.ITemperatureSensorInfo)

    @property
    def tempString(self):
        tc = self._object.temperatureCelsiusString()
	tf = self._object.temperatureFahrenheitString()
	if tc == tf: return tc
        return tc + " / " + tf

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class PowerSupplyInfo(ComponentInfo):
    implements(interfaces.IPowerSupplyInfo)
    
    type = ProxyProperty("type")

    @property
    def wattsString(self):
        return self._object.wattsString()

    @property
    def millivoltsString(self):
        return self._object.millivoltsString()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

