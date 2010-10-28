################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.DellEqualLogicMon import interfaces

class DellEqualLogicStoragePoolInfo(ComponentInfo):
    implements(interfaces.IDellEqualLogicStoragePoolInfo)

    description = ProxyProperty("description")

    @property
    def name(self):
        return self._object.caption

    @property
    def totalBytesString(self):
        return self._object.totalBytesString()

    @property
    def usedBytesString(self):
        return self._object.usedBytesString()

class DellEqualLogicVolumeInfo(ComponentInfo):
    implements(interfaces.IDellEqualLogicVolumeInfo)

    description = ProxyProperty("description")

    @property
    def name(self):
	return self._object.caption
 
    @property
    def provisionedSizeString(self):
        return self._object.provisionedSizeString()

    @property
    def reservedSizeString(self):
	return self._object.reservedSizeString()

    @property
    def isThinProvisioned(self):
	return self._object.isThinProvisioned()
