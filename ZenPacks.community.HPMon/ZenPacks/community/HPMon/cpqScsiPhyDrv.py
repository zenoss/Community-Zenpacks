################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqScsiPhyDrv

cpqScsiPhyDrv is an abstraction of a HP SCSI Hard Disk.

$Id: cpqScsiPhyDrv.py,v 1.0 2009/03/10 12:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.HPMon.HPHardDisk import HPHardDisk

class cpqScsiPhyDrv(HPHardDisk):
    """cpqScsiPhyDrv object
    statusmap(statusDot, statusSeveriry, statusString)
    statusDot(0:'green', 1:'yellow', 2:'orange', 3:'red', 4:'grey')
    statusSeverity(0:'Clean', 1:'Debug', 2:'Info', 3:'Warning', 4:'Error', 5:'Critical')
    """

    portal_type = meta_type = 'cpqScsiPhyDrv'

    statusmap = [(4, 3, 'other'),
	        (4, 3, 'other'),
		(0, 0, 'Ok'),
		(3, 5, 'Failed'),
		(1, 3, 'Not Configured'),
		(2, 4, 'Bad Cable'),
		(3, 5, 'Missing was Ok'),
		(3, 5, 'Missing was Failed'),
		(2, 4, 'Predictive Failure'),
		(3, 5, 'Missing was Predictive Failure'),
		(3, 5, 'Offline'),
		(3, 5, 'Missing was Offline'),
		(3, 5, 'Hard Error'),
		]

InitializeClass(cpqScsiPhyDrv)
