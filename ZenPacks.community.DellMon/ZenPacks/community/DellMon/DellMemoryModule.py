################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellMemoryModule

DellMemoryModule is an abstraction of a  Memory Module.

$Id: DellMemoryModule.py,v 1.1 2010/06/30 22:05:40 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.MemoryModule import *
from DellComponent import *

class DellMemoryModule(MemoryModule, DellComponent):
    """MemoryModule object"""

    status = 1
    speed = ""

    _properties = MemoryModule._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
        {'id':'speed', 'type':'string', 'mode':'w'},
    )

    def speedString(self):
        return self.speed

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(DellMemoryModule)
