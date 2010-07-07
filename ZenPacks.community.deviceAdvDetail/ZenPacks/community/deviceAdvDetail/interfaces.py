################################################################################
#
# This program is part of the deviceAdvDetail Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.1 2010/07/07 13:37:53 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.Zuul.interfaces import IThresholdInfo, IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IStatusThresholdInfo(IThresholdInfo):
    """
    Adapts the StatusThresholdClass
    """
    escalateCount = schema.Int(title=_t(u'Escalate Count'), order=7)


class IMemoryModuleInfo(IComponentInfo):
    """
    Info adapter for MemoryModule components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    size = schema.Int(title=u"Size", readonly=True, group='Details')

class ILogicalDiskInfo(IComponentInfo):
    """
    Info adapter for LogicalDisk components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    description = schema.Text(title=u"OS Name", readonly=True,
                                group='Details')
    diskType = schema.Text(title=u"Type", readonly=True, group='Details')
    stripesize = schema.Int(title=u"Stripe Size", readonly=True, group='Details')
    size = schema.Int(title=u"Size", readonly=True, group='Details')


class IExpansionCardInfo(IComponentInfo):
    """
    Info adapter for ExpansionCard components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')


class IHardDiskInfo(IComponentInfo):
    """
    Info adapter for HardDisk components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True, group='Details')
    FWRev = schema.Text(title=u"Firmware", readonly=True, group='Details')
    size = schema.Int(title=u"Size", readonly=True, group='Details')
    diskType = schema.Text(title=u"Type", readonly=True, group='Details')
    rpm = schema.Int(title=u"RPM", readonly=True, group='Details')
    bay = schema.Int(title=u"Bay", readonly=True, group='Details')

class IFanInfo(IComponentInfo):
    """
    Info adapter for Fan components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    rpmString = schema.Text(title=u"Speed", readonly=True, group='Overview')

class ITemperatureSensorInfo(IComponentInfo):
    """
    Info adapter for TemperatureSensor components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    tempString = schema.Text(title=u"Temperature", readonly=True, group='Overview')

class IPowerSupplyInfo(IComponentInfo):
    """
    Info adapter for PowerSupply components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    type = schema.Text(title=u"Type", readonly=True, group='Details')
    wattsString = schema.Text(title=u"Watts", readonly=True, group='Details')
    millivoltsString = schema.Text(title=u"Voltage", readonly=True, group='Details')
