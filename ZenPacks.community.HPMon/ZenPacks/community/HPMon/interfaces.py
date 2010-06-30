################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.0 2010/06/24 12:31:06 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IcpqIdeControllerInfo(IComponentInfo):
    """
    Info adapter for cpqIdeController components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')
    FWRev = schema.Text(title=u"Firmware", readonly=True, group='Details')

class IcpqScsiCntlrInfo(IcpqIdeControllerInfo):
    """
    Info adapter for cpqScsiCntlr components.
    """
    scsiwidth = schema.Text(title=u"SCSI Bus Width", readonly=True, group='Details')

class IcpqDaCntlrInfo(IcpqIdeControllerInfo):
    """
    Info adapter for cpqDaCntlr components.
    """
    redundancyType = schema.Text(title=u"Redundancy Type", readonly=True, group='Details')
    roleString = schema.Text(title=u"Current Role", readonly=True, group='Details')
    
class IcpqFcTapeCntlrInfo(IcpqIdeControllerInfo):
    """
    Info adapter for cpqFcTapeCntlr components.
    """
    wwn = schema.Text(title=u"World Wide Node Name", readonly=True, group='Details')
    
class IcpqFcaCntlrInfo(IcpqIdeControllerInfo):
    """
    Info adapter for cpqFcaCntlr components.
    """
    redundancyType = schema.Text(title=u"Redundancy Type", readonly=True, group='Details')
    roleString = schema.Text(title=u"Current Role", readonly=True, group='Details')
    wwnn = schema.Text(title=u"World Wide Node Name", readonly=True, group='Details')
    wwpn = schema.Text(title=u"World Wide Port Name", readonly=True, group='Details')
    
class IcpqFcaHostCntlrInfo(IcpqIdeControllerInfo):
    """
    Info adapter for cpqFcaHostCntlr components.
    """
    ROMRev = schema.Text(title=u"ROM Version", readonly=True, group='Details')
    wwnn = schema.Text(title=u"World Wide Node Name", readonly=True, group='Details')
    wwpn = schema.Text(title=u"World Wide Port Name", readonly=True, group='Details')
    
class IcpqNicIfPhysAdapterInfo(IComponentInfo):
    """
    Info adapter for cpqNicIfPhysAdapter components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')
    port = schema.Int(title=u"Port", readonly=True, group='Details')
    speed = schema.Text(title=u"Speed", readonly=True, group='Details')
    duplex = schema.Text(title=u"Duplex", readonly=True, group='Details')
    role = schema.Text(title=u"Role", readonly=True, group='Details')
    macaddress = schema.Text(title=u"MAC Address", readonly=True, group='Details')

class IcpqSm2CntlrInfo(IComponentInfo):
    """
    Info adapter for cpqSm2Cntlr components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')
    romRev = schema.Text(title=u"ROM Version", readonly=True, group='Details')
    hwVer = schema.Text(title=u"Hardware Version", readonly=True, group='Details')
    systemId = schema.Text(title=u"System ID", readonly=True, group='Details')
    macaddress = schema.Text(title=u"MAC Address", readonly=True, group='Network Settings')
    ipaddress = schema.Text(title=u"IP Address", readonly=True, group='Network Settings')
    subnetmask = schema.Text(title=u"Subnet Mask", readonly=True, group='Network Settings')
    dnsName = schema.Text(title=u"DNS Name", readonly=True, group='Network Settings')
