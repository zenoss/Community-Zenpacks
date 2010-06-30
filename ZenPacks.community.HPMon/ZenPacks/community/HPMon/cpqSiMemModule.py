################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqSiMemModule

cpqSiMemModule is an abstraction of a  Memory Module.

$Id: cpqSiMemModule.py,v 1.1 2010/06/29 12:24:12 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.MemoryModule import *
from HPComponent import *

class cpqSiMemModule(MemoryModule, HPComponent):
    """MemoryModule object"""

    portal_type = meta_type = 'MemoryModule'

    status = 1

    # we monitor Memory modules
    monitor = True

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
                2: (DOT_GREY, SEV_WARNING, 'Not Present'),
                3: (DOT_YELLOW, SEV_WARNING, 'Present'),
                4: (DOT_GREEN, SEV_CLEAN, 'Good'),
                5: (DOT_YELLOW, SEV_WARNING, 'Add'),
                6: (DOT_YELLOW, SEV_WARNING, 'Upgraded'),
                7: (DOT_RED, SEV_CRITICAL, 'Missing'),
                8: (DOT_RED, SEV_CRITICAL, 'Dos not Match'),
                9: (DOT_RED, SEV_CRITICAL, 'Not Supported'),
                10:(DOT_RED, SEV_CRITICAL, 'Bad Config'),
                11:(DOT_ORANGE, SEV_ERROR, 'Degraded'),
                }

    _properties = MemoryModule._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(cpqSiMemModule)
