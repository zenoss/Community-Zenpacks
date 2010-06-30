################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
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
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.community.HPMon import interfaces


class cpqIdeControllerInfo(ComponentInfo):
    implements(interfaces.IcpqIdeControllerInfo)

    serialNumber = ProxyProperty("serialNumber")
    FWRev = ProxyProperty("FWRev")
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


class cpqSasHbaInfo(ComponentInfo):
    implements(interfaces.IcpqIdeControllerInfo)


class cpqScsiCntlrInfo(cpqIdeControllerInfo):
    implements(interfaces.IcpqScsiCntlrInfo)

    scsiwidth = ProxyProperty("scsiwidth")

class cpqDaCntlrInfo(cpqIdeControllerInfo):
    implements(interfaces.IcpqDaCntlrInfo)

    redundancyType = ProxyProperty("redundancyType")

    @property
    def roleString(self):
        return self._object.roleString()

class cpqFcTapeCntlrInfo(cpqIdeControllerInfo):
    implements(interfaces.IcpqFcTapeCntlrInfo)

    wwn = ProxyProperty("wwn")

class cpqFcaCntlrInfo(cpqIdeControllerInfo):
    implements(interfaces.IcpqFcaCntlrInfo)

    wwnn = ProxyProperty("wwnn")
    wwpn = ProxyProperty("wwpn")
    redundancyType = ProxyProperty("redundancyType")

    @property
    def roleString(self):
        return self._object.roleString()

    @property
    def slot(self):
        return self._object.boxIoSlot()

class cpqFcaHostCntlrInfo(cpqIdeControllerInfo):
    implements(interfaces.IcpqFcaHostCntlrInfo)

    ROMRev = ProxyProperty("ROMRev")
    wwnn = ProxyProperty("wwnn")
    wwpn = ProxyProperty("wwpn")

class cpqNicIfPhysAdapterInfo(ComponentInfo):
    implements(interfaces.IcpqNicIfPhysAdapterInfo)

    serialNumber = ProxyProperty("serialNumber")
    slot = ProxyProperty("slot")
    port = ProxyProperty("port")
    role = ProxyProperty("role")
    macaddress = ProxyProperty("macaddress")
    duplex = ProxyProperty("duplex")

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
    def speed(self):
        return self._object.speedString()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

class cpqSm2CntlrInfo(ComponentInfo):
    implements(interfaces.IcpqSm2CntlrInfo)

    slot = ProxyProperty("slot")
    serialNumber = ProxyProperty("serialNumber")
    romRev = ProxyProperty("romRev")
    hwVer = ProxyProperty("hwVer")
    systemId = ProxyProperty("systemId")
    macaddress = ProxyProperty("macaddress")
    ipaddress = ProxyProperty("ipaddress")
    subnetmask = ProxyProperty("subnetmask")
    dnsName = ProxyProperty("dnsName")

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
