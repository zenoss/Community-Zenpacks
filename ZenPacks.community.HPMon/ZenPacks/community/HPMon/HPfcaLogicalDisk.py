################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPfcaLogicalDisk

HPfcaLogicalDisk is an abstraction of a harddisk.

$Id: HPfcaLogicalDisk.py,v 1.0 2009/03/10 12:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.HPMon.HPLogicalDisk import HPLogicalDisk

class HPfcaLogicalDisk(HPLogicalDisk):
    """HPfcaLogicalDisk object
    statusmap(statusDot, statusSeveriry, statusString)
    statusDot(0:'green', 1:'yellow', 2:'orange', 3:'red', 4:'grey')
    statusSeverity(0:'Clean', 1:'Debug', 2:'Info', 3:'Warning', 4:'Error', 5:'Critical')
    """

    portal_type = meta_type = 'HPfcaLogicalDisk'

    statusmap = [(4, 3, 'other'),
	        (4, 3, 'other'),
		(0, 0, 'Ok'),
		(3, 5, 'Failed'),
		(1, 3, 'Unconfigured'),
		(2, 4, 'Recovering'),
		(1, 3, 'Ready Rebuild'),
		(1, 3, 'Rebuilding'),
		(2, 4, 'Wrong Drive'),
		(2, 4, 'Bad Connect'),
		(3, 5, 'Overheating'),
		(3, 5, 'Shutdown'),
		(1, 3, 'Expanding'),
		(1, 3, 'Not Available'),
		(1, 3, 'Queued For Expansion'),
		(3, 5, 'Hard Error'),
		]

InitializeClass(HPfcaLogicalDisk)
