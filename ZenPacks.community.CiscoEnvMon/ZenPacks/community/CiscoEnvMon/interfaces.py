################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.1 2010/12/14 22:00:44 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.Zuul.interfaces import IThresholdInfo, IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class ICiscoExpansionCardInfo(IComponentInfo):
    """
    Info adapter for CiscoExpansionCard components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                                            group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True, group='Details')
    partNumber = schema.Text(title=u"Part #", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')
    HWVer = schema.Int(title=u"HW Version", readonly=True, group='Details')
    SWVer = schema.Int(title=u"SW Version", readonly=True, group='Details')
    FWRev = schema.Int(title=u"Firmware", readonly=True, group='Details')


class ICiscoFanInfo(IComponentInfo):
    """
    Info adapter for CiscoFan components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    rpmString = schema.Text(title=u"Speed", readonly=True, group='Overview')

class ICiscoTemperatureSensorInfo(IComponentInfo):
    """
    Info adapter for CiscoTemperatureSensor components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    tempString = schema.Text(title=u"Temperature", readonly=True, group='Overview')

class ICiscoPowerSupplyInfo(IComponentInfo):
    """
    Info adapter for CiscoPowerSupply components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    type = schema.Text(title=u"Type", readonly=True, group='Details')
    wattsString = schema.Text(title=u"Watts", readonly=True, group='Details')
    millivoltsString = schema.Text(title=u"Voltage", readonly=True, group='Details')
