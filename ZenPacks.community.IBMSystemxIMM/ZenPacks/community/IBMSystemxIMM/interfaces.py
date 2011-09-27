# ==============================================================================
# Zenoss community Zenpack for IBM SystemX Integrated Management Module
# version: 1.0
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

__doc__="""interfaces describes the form field to the user interface"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "1.0.0"

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IIMMFwVpdInfo(IComponentInfo):

    immVpdIndex = schema.Text(title=u"ID", readonly=True, group='Details')
    immVpdType = schema.Text(title=u"Firmware VPD Type", readonly=True, group='Details')
    immVpdVersionString = schema.Text(title=u"Version", readonly=True,group='Details')
    immVpdReleaseDate = schema.Text(title=u"Release Date", readonly=True, group='Details')
    comment = schema.Text(title=u"Comment", group='Details')

class IIMMCpuVpdInfo(IComponentInfo):

    cpuVpdIndex = schema.Text(title=u"ID", readonly=True, group='Details')
    cpuVpdDescription = schema.Text(title=u"Description", readonly=True, group='Details')
    cpuVpdSpeed = schema.Text(title=u"Speed (MHz)", readonly=True,group='Details')
    cpuVpdIdentifier = schema.Text(title=u"Identifier", readonly=True,group='Details')
    cpuVpdType = schema.Text(title=u"Type", readonly=True,group='Details')
    cpuVpdFamily = schema.Text(title=u"Family", readonly=True,group='Details')
    cpuVpdCores = schema.Text(title=u"Cores", readonly=True,group='Details')
    cpuVpdThreads = schema.Text(title=u"Threads", readonly=True, group='Details')
    cpuVpdVoltage = schema.Text(title=u"Voltage", readonly=True, group='Details')
    cpuVpdDataWidth = schema.Text(title=u"Data Width", readonly=True, group='Details')

class IIMMMemVpdInfo(IComponentInfo):

    memoryVpdIndex = schema.Text(title=u"ID", readonly=True, group='Details')
    memoryVpdDescription = schema.Text(title=u"Description", readonly=True, group='Details')
    memoryVpdPartNumber = schema.Text(title=u"Part Number", readonly=True,group='Details')
    memoryVpdFRUSerialNumber = schema.Text(title=u"Serial Number", readonly=True,group='Details')
    memoryVpdManufactureDate = schema.Text(title=u"Manufacture date", readonly=True,group='Details')
    memoryVpdType = schema.Text(title=u"Memory type", readonly=True,group='Details')
    memoryVpdSize = schema.Text(title=u"Size (GB)", readonly=True,group='Details')

class IIMMComponentVpdInfo(IComponentInfo):

    componentLevelVpdIndex = schema.Text(title=u"ID", readonly=True, group='Details')
    componentLevelVpdFruNumber = schema.Text(title=u"FRU Number", readonly=True, group='Details')
    componentLevelVpdFruName = schema.Text(title=u"FRU Name", readonly=True,group='Details')
    componentLevelVpdSerialNumber = schema.Text(title=u"Serial Number", readonly=True,group='Details')
    componentLevelVpdManufacturingId = schema.Text(title=u"Manufacturer", readonly=True,group='Details')

class IIMMComponentLogInfo(IComponentInfo):

    componentLevelVpdTrackingIndex = schema.Text(title=u"ID", readonly=True, group='Details')
    componentLevelVpdTrackingFruNumber = schema.Text(title=u"FRU Number", readonly=True, group='Details')
    componentLevelVpdTrackingFruName = schema.Text(title=u"FRU Name", readonly=True,group='Details')
    componentLevelVpdTrackingSerialNumber = schema.Text(title=u"Serial Number", readonly=True,group='Details')
    componentLevelVpdTrackingManufacturingId = schema.Text(title=u"Manufacturer", readonly=True,group='Details')
    componentLevelVpdTrackingAction = schema.Text(title=u"Action", readonly=True,group='Details')
    componentLevelVpdTrackingTimestamp = schema.Text(title=u"Timestamp", readonly=True,group='Details')

class IIMMFanMonInfo(IComponentInfo):

    fanIndex = schema.Text(title=u"ID", readonly=True, group='Details')
    fanDescr = schema.Text(title=u"Fan Description", readonly=True, group='Details')
    fanSpeed = schema.Text(title=u"Fan Speed", readonly=True,group='Details')
    fanCritLimitLow = schema.Text(title=u"Critical Low Limit", readonly=True,group='Details')

class IIMMVoltMonInfo(IComponentInfo):

    voltIndex = schema.Text(title=u"ID", readonly=True, group='Details')
    voltDescr = schema.Text(title=u"Description", readonly=True, group='Details')
    voltReading = schema.Text(title=u"Current Reading", readonly=True,group='Details')
    voltNominalReading = schema.Text(title=u"Nominal Reading", readonly=True,group='Details')
    voltCritLimitHigh = schema.Text(title=u"Critical High Limit", readonly=True,group='Details')
    voltCritLimitLow = schema.Text(title=u"Critical Low Limit", readonly=True,group='Details')
