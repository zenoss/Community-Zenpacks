################################################################################
#
# This program is part of the DelliEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Pnns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenModel.Fan import *
from ZenPacks.community.deviceAdvDetail.HWStatus import *

class DellEqualLogicFan(Fan, HWStatus):
    """Fan object"""

    statusmap ={0: (DOT_GREY, SEV_WARNING, 'Unknown'),
                1: (DOT_GREEN, SEV_CLEAN, 'Normal'),
                2: (DOT_YELLOW, SEV_WARNING, 'Warning'),
                3: (DOT_RED, SEV_CRITICAL, 'Critical'),
                }

    status = 1
    lowThreshold = 0
    highThreshold = 0

    _properties = Fan._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 {'id':'lowThreshold', 'type':'int', 'mode':'w'},
                 {'id':'highThreshold', 'type':'int', 'mode':'w'},
                )

    def setState(self, value):
        self.status = 0
        for intvalue, status in self.statusmap.iteritems():
            if status[2].upper() != value.upper(): continue
            self.status = value
            break

    state = property(fget=lambda self: self.statusString(),
                     fset=lambda self, v: self.setState(v)
                     )

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(DellEqualLogicFan)
