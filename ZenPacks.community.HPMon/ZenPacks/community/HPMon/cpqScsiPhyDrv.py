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

from HPHardDisk import *

class cpqScsiPhyDrv(HPHardDisk):
    """cpqScsiPhyDrv object
    """

    portal_type = meta_type = 'cpqScsiPhyDrv'

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
		2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
		3: (DOT_RED, SEV_CRITICAL, 'Failed'),
		4: (DOT_YELLOW, SEV_WARNING, 'Not Configured'),
		5: (DOT_ORANGE, SEV_ERROR, 'Bad Cable'),
		6: (DOT_RED, SEV_CRITICAL, 'Missing was Ok'),
		7: (DOT_RED, SEV_CRITICAL, 'Missing was Failed'),
		8: (DOT_ORANGE, SEV_ERROR, 'Predictive Failure'),
		9: (DOT_RED, SEV_CRITICAL, 'Missing was Predictive Failure'),
		10:(DOT_RED, SEV_CRITICAL, 'Offline'),
		11:(DOT_RED, SEV_CRITICAL, 'Missing was Offline'),
		12:(DOT_RED, SEV_CRITICAL, 'Hard Error'),
		}

InitializeClass(cpqScsiPhyDrv)
