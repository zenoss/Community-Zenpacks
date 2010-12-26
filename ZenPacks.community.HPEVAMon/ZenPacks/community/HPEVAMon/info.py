################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of HPEVA components.

$Id: info.py,v 1.2 2010/11/30 20:45:46 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.HPEVAMon import interfaces


class HPEVADiskDriveInfo(ComponentInfo):
    implements(interfaces.IHPEVADiskDriveInfo)

    serialNumber = ProxyProperty("serialNumber")
    diskType = ProxyProperty("diskType")
    size = ProxyProperty("size")
    FWRev = ProxyProperty("FWRev")
    bay = ProxyProperty("bay")
    wwn = ProxyProperty("wwn")

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
    @info
    def enclosure(self):
        return self._object.getEnclosure()

    @property
    @info
    def storagePool(self):
        return self._object.getStoragePool()

    @property
    def name(self):
        return self._object.description

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()


class HPEVAHostFCPortInfo(ComponentInfo):
    implements(interfaces.IHPEVAHostFCPortInfo)

    fc4Types = ProxyProperty("fc4Types")
    fullDuplex = ProxyProperty("fullDuplex")
    linkTechnology = ProxyProperty("linkTechnology")
    networkAddresses = ProxyProperty("networkAddresses")
    type = ProxyProperty("type")
    description = ProxyProperty("description")
    mtu = ProxyProperty("mtu")
    wwn = ProxyProperty("wwn")

    @property
    def name(self):
        return self._object.interfaceName

    @property
    def speed(self):
        return self._object.speedString()

    @property
    @info
    def controller(self):
        return self._object.getController()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

class HPEVAStorageDiskEnclosureInfo(ComponentInfo):
    implements(interfaces.IHPEVAStorageDiskEnclosureInfo)

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

class HPEVAStoragePoolInfo(ComponentInfo):
    implements(interfaces.IHPEVAStoragePoolInfo)

    diskGroupType = ProxyProperty("diskGroupType")
    diskType = ProxyProperty("diskType")
    protLevel = ProxyProperty("protLevel")
    totalDisks = ProxyProperty("totalDisks")

    @property
    def name(self):
        return self._object.caption

    @property
    def totalBytesString(self):
        return self._object.totalBytesString()

    @property
    def usedBytesString(self):
        return self._object.usedBytesString()

    @property
    def availBytesString(self):
        return self._object.availBytesString()

    @property
    def capacity(self):
        return self._object.capacity()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

class HPEVAStorageProcessorCardInfo(ComponentInfo):
    implements(interfaces.IHPEVAStorageProcessorCardInfo)

    slot = ProxyProperty("slot")
    serialNumber = ProxyProperty("serialNumber")
    FWRev = ProxyProperty("FWRev")

    @property
    def name(self):
        return self._object.caption

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
    def uptime(self):
        return self._object.uptimeString()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

class HPEVAStorageVolumeInfo(ComponentInfo):
    implements(interfaces.IHPEVAStorageVolumeInfo)

    preferredPath = ProxyProperty("preferredPath")
    accessType = ProxyProperty("accessType")
    raidType = ProxyProperty("raidType")
    diskType = ProxyProperty("diskType")
    mirrorCache = ProxyProperty("mirrorCache")
    readCachePolicy = ProxyProperty("readCachePolicy")
    writeCachePolicy = ProxyProperty("writeCachePolicy")

    @property
    def name(self):
        return self._object.caption

    @property
    def totalBytesString(self):
        return self._object.totalBytesString()

    @property
    @info
    def storagePool(self):
        return self._object.getStoragePool()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

class HPEVAConsistencySetInfo(ComponentInfo):
    implements(interfaces.IHPEVAConsistencySetInfo)

    participationType = ProxyProperty("participationType")
    writeMode = ProxyProperty("writeMode")
    remoteCellName = ProxyProperty("remoteCellName")
    hostAccessMode = ProxyProperty("hostAccessMode")
    failSafe = ProxyProperty("failSafe")
    suspendMode = ProxyProperty("suspendMode")

    @property
    def name(self):
        return self._object.caption

    @property
    @info
    def storagePool(self):
        return self._object.getStoragePool()

    @property
    def currentPercentLogLevel(self):
        return self._object.getCurrentPercentLogLevel()

    @property
    def logDiskReservedCapacity(self):
        return self._object.getLogDiskReservedCapacity()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

