# ==============================================================================
# Zenoss community Zenpack for IBM SystemX Integrated Management Module
# version: 0.3
#
# (C) Copyright IBM Corp. 2011. All Rights Reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ==============================================================================

__doc__="""Representation of IMM VPD and Monitoring components"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "0.3.0"

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
#from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.IBMSystemxIMM import interfaces

class IMMFwVpdInfo(ComponentInfo):
    implements(interfaces.IIMMFwVpdInfo)

    immVpdIndex = ProxyProperty("immVpdIndex")
    immVpdType = ProxyProperty("immVpdType")
    immVpdVersionString = ProxyProperty("immVpdVersionString")
    immVpdReleaseDate = ProxyProperty("immVpdReleaseDate")
    comment = ProxyProperty("comment")

class IMMCpuVpdInfo(ComponentInfo):
    implements(interfaces.IIMMCpuVpdInfo)

    cpuVpdIndex = ProxyProperty("cpuVpdIndex")
    cpuVpdDescription = ProxyProperty("cpuVpdDescription")
    cpuVpdSpeed = ProxyProperty("cpuVpdSpeed")
    cpuVpdIdentifier = ProxyProperty("cpuVpdIdentifier")
    cpuVpdType = ProxyProperty("cpuVpdType")
    cpuVpdFamily = ProxyProperty("cpuVpdFamily")
    cpuVpdCores = ProxyProperty("cpuVpdCores")
    cpuVpdThreads = ProxyProperty("cpuVpdThreads")
    cpuVpdVoltage = ProxyProperty("cpuVpdVoltage")
    cpuVpdDataWidth = ProxyProperty("cpuVpdDataWidth")

class IMMMemVpdInfo(ComponentInfo):
    implements(interfaces.IIMMMemVpdInfo)

    memoryVpdIndex = ProxyProperty("memoryVpdIndex")
    memoryVpdDescription = ProxyProperty("memoryVpdDescription")
    memoryVpdPartNumber = ProxyProperty("memoryVpdPartNumber")
    memoryVpdFRUSerialNumber = ProxyProperty("memoryVpdFRUSerialNumber")
    memoryVpdManufactureDate = ProxyProperty("memoryVpdManufactureDate")
    memoryVpdType = ProxyProperty("memoryVpdType")
    memoryVpdSize = ProxyProperty("memoryVpdSize")

class IMMComponentVpdInfo(ComponentInfo):
    implements(interfaces.IIMMComponentVpdInfo)

    componentLevelVpdIndex = ProxyProperty("componentLevelVpdIndex")
    componentLevelVpdFruNumber = ProxyProperty("componentLevelVpdFruNumber")
    componentLevelVpdFruName = ProxyProperty("componentLevelVpdFruName")
    componentLevelVpdSerialNumber = ProxyProperty("componentLevelVpdSerialNumber")
    componentLevelVpdManufacturingId = ProxyProperty("componentLevelVpdManufacturingId")

class IMMComponentLogInfo(ComponentInfo):
    implements(interfaces.IIMMComponentLogInfo)

    componentLevelVpdTrackingIndex = ProxyProperty("componentLevelVpdTrackingIndex")
    componentLevelVpdTrackingFruNumber = ProxyProperty("componentLevelVpdTrackingFruNumber")
    componentLevelVpdTrackingFruName = ProxyProperty("componentLevelVpdTrackingFruName")
    componentLevelVpdTrackingSerialNumber = ProxyProperty("componentLevelVpdTrackingSerialNumber")
    componentLevelVpdTrackingManufacturingId = ProxyProperty("componentLevelVpdTrackingManufacturingId")
    componentLevelVpdTrackingAction = ProxyProperty("componentLevelVpdTrackingAction")
    componentLevelVpdTrackingTimestamp = ProxyProperty("componentLevelVpdTrackingTimestamp")

class IMMFanMonInfo(ComponentInfo):
    implements(interfaces.IIMMFanMonInfo)

    fanIndex = ProxyProperty("fanIndex")
    fanDescr = ProxyProperty("fanDescr")
    fanSpeed = ProxyProperty("fanSpeed")
    fanCritLimitLow = ProxyProperty("fanCritLimitLow")

class IMMVoltMonInfo(ComponentInfo):
    implements(interfaces.IIMMVoltMonInfo)

    voltIndex = ProxyProperty("voltIndex")
    voltDescr = ProxyProperty("voltDescr")
    voltReading = ProxyProperty("voltReading")
    voltNominalReading = ProxyProperty("voltNominalReading")
    voltCritLimitHigh = ProxyProperty("voltCritLimitHigh")
    voltCritLimitLow = ProxyProperty("voltCritLimitLow")
