################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IDellEqualLogicStoragePoolInfo(IComponentInfo):
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    totalBytesString = schema.Text(title=u"Total Bytes", readonly=True, group="Details")
    usedBytesString = schema.Text(title=u"Used Bytes", readonly=True, group="Details")

class IDellEqualLogicVolumeInfo(IComponentInfo):
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    provisionedSizeString = schema.Text(title=u"Provisioned Size", readonly=True, group="Details")
    reservedSizeString = schema.Text(title=u"Reserved Size", readonly=True, group="Details")    
    isThinProvisioned = schema.Text(title=u"Thin Provisioned", readonly=True, group="Details")
