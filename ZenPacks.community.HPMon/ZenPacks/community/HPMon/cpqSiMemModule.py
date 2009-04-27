################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqSiMemModule

cpqSiMemModule is an abstraction of a  Memory Module.

$Id: cpqSiMemModule.py,v 1.0 2008/12/03 08:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.MemoryModule import *
from HPComponent import *

class cpqSiMemModule(MemoryModule, HPComponent):
    """MemoryModule object"""

    portal_type = meta_type = 'cpqSiMemModule'

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

InitializeClass(cpqSiMemModule)
