################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.2 2010/11/30 20:46:34 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IHPEVADiskDriveInfo(IComponentInfo):
    """
    Info adapter for HPEVA Disk Drive components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True,group='Details')
    FWRev = schema.Text(title=u"Firmware", readonly=True, group='Details')
    size = schema.Int(title=u"Size", readonly=True, group='Details')
    diskType = schema.Text(title=u"Type", readonly=True, group='Details')
    enclosure = schema.Entity(title=u"Enclosure", readonly=True,group='Details')
    bay = schema.Int(title=u"Bay", readonly=True, group='Details')
    storagePool = schema.Entity(title=u"Disk Group", readonly=True,
                                                                group='Details')
    wwn = schema.Text(title=u"WWN", readonly=True, group='Details')

class IHPEVAHostFCPortInfo(IComponentInfo):
    """
    Info adapter for HPEVA Host FC Port components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    name = schema.Text(title=u"Interface Name", readonly=True, group='Overview')
    controller = schema.Entity(title=u"Storage Controller", readonly=True,
                                                                group='Details')
    fc4Types = schema.List(title=u"Active FC4 types", readonly=True,
                                                                group='Details')
    fullDuplex = schema.Bool(title=u"Duplex", readonly=True, group='Details')
    linkTechnology = schema.Text(title=u"Link Technology", readonly=True,
                                                                group='Details')
    networkAddresses = schema.List(title=u"networkAddresses", readonly=True,
                                                                group='Details')
    type = schema.Text(title=u"Type", readonly=True, group='Details')
    speed = schema.Text(title=u"Speed", readonly=True, group='Details')
    mtu = schema.Int(title=u"MTU", readonly=True, group='Details')
    wwn = schema.Text(title=u"WWN", readonly=True, group='Details')

class IHPEVAStorageDiskEnclosureInfo(IComponentInfo):
    """
    Info adapter for HPEVA Storage Disk Enclosure components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')

class IHPEVAStoragePoolInfo(IComponentInfo):
    """
    Info adapter for HPEVA Disk Groups components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    totalDisks = schema.Int(title=u"Total Disk", group="Details")
    diskGroupType = schema.Text(title=u"Disk Group Type", group="Details")
    diskType = schema.Text(title=u"Disk Type", group="Details")
    protLevel = schema.Text(title=u"Protection Level", group="Details")
    totalBytesString = schema.Text(title=u"Total Bytes", readonly=True,
                                                                group="Details")
    usedBytesString = schema.Text(title=u"Used Bytes", readonly=True,
                                                                group="Details")
    availBytesString = schema.Text(title=u"Available Bytes", readonly=True,
                                                                group="Details")
    capacity = schema.Text(title=u"Capacity Bytes", readonly=True,
                                                                group="Details")

class IHPEVAStorageProcessorCardInfo(IComponentInfo):
    """
    Info adapter for HPEVA Storage Processor Card components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    uptime = schema.Text(title=u"Uptime", readonly=True, group='Overview')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True,
                                                                group='Details')
    FWRev = schema.Text(title=u"Firmware", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=True, group='Details')

class IHPEVAStorageVolumeInfo(IComponentInfo):
    """
    Info adapter for HPEVA Storage Volume components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    storagePool = schema.Entity(title=u"Disk Group", readonly=True,
                                                                group='Details')
    preferredPath = schema.Text(title=u"Preferred Path", readonly=True,
                                                                group='Details')
    accessType = schema.Text(title=u"Access Type", readonly=True,
                                                                group='Details')
    raidType = schema.Text(title=u"RAID Type", readonly=True, group='Details')
    diskType = schema.Text(title=u"Disk Type", readonly=True, group='Details')
    mirrorCache = schema.Text(title=u"Mirror Cache", readonly=True,
                                                                group='Details')
    readCachePolicy = schema.Text(title=u"Read Cache Policy", readonly=True,
                                                                group='Details')
    writeCachePolicy = schema.Text(title=u"Write Cache Policy", readonly=True,
                                                                group='Details')
    totalBytesString = schema.Text(title=u"Total Bytes", readonly=True,
                                                                group="Details")

class IHPEVAConsistencySetInfo(IComponentInfo):
    """
    Info adapter for HPEVA DR Group components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    participationType = schema.Text(title=u"Role",readonly=True,group='Details')
    writeMode = schema.Text(title=u"Write Mode", readonly=True, group='Details')
    storagePool = schema.Entity(title=u"Log Disk Group", readonly=True,
                                                                group='Details')
    logDiskReservedCapacity = schema.Entity(title=u"Log Disk Reserved Capacity",
                                                readonly=True, group='Details')
    currentPercentLogLevel = schema.Text(title=u"Log Usage", readonly=True,
                                                                group='Details')
    remoteCellName = schema.Text(title=u"Remote System", readonly=True,
                                                                group='Details')
    hostAccessMode = schema.Text(title=u"Host Access Mode", readonly=True,
                                                                group='Details')
    failSafe = schema.Text(title=u"Failsafe", readonly=True, group='Details')
    suspendMode = schema.Text(title=u"Suspend Mode", readonly=True,
                                                                group='Details')
