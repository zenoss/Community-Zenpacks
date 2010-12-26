################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.2 2010/10/19 23:46:33 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IDellStorageCntlrInfo(IComponentInfo):
    """
    Info adapter for DellStorageCntlr components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')
    controllerType = schema.Text(title=u"Type", readonly=True, group='Details')
    role = schema.Text(title=u"Role", readonly=True, group='Details')
    FWRev = schema.Text(title=u"Firmware Revision", readonly=True, group='Details')
    SWVer = schema.Text(title=u"Driver Version", readonly=True, group='Details')
    cacheSize = schema.Int(title=u"Cache Size", readonly=True, group='Details')

class IDellRemoteAccessCntlrInfo(IComponentInfo):
    """
    Info adapter for DellRemoteAccessCntlr components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')
    FWRev = schema.Text(title=u"Firmware Revision", readonly=True,
                                group='Details')
    SWVer = schema.Text(title=u"Drivers Pack Version", readonly=True, group='Details')
    ipaddress = schema.Text(title=u"IP Address", readonly=True,
                                group='Network Settings')
    subnetmask = schema.Text(title=u"Subnet Mask", readonly=True,
                                group='Network Settings')
    macaddress = schema.Text(title=u"IP Address", readonly=True,
                                group='Network Settings')
