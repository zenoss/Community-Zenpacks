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

from Globals import InitializeClass
from MemoryModule import MemoryModule
from HPComponent import HPComponent

class cpqSiMemModule(MemoryModule, HPComponent):
    """MemoryModule object"""

    portal_type = meta_type = 'cpqSiMemModule'

    status = 1
        
    # we monitor Memory modules
    monitor = True

    statusmap = [(4, 3, 'other'),
	        (4, 3, 'other'),
	        (4, 3, 'Not Present'),
		(1, 3, 'Present'),
		(0, 0, 'Good'),
		(1, 3, 'Add'),
		(1, 3, 'Upgraded'),
		(3, 5, 'Missing'),
		(3, 5, 'Dos not Match'),
		(3, 5, 'Not Supported'),
		(3, 5, 'Bad Config'),
		(2, 4, 'Degraded'),
		]
    
    _properties = MemoryModule._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
    )

InitializeClass(cpqSiMemModule)
