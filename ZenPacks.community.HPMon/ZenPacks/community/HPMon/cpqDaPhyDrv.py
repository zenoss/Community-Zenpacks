################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqDaPhyDrv

cpqDaPhyDrv is an abstraction of a HP DA Hard Disk.

$Id: cpqDaPhyDrv.py,v 1.0 2009/03/10 12:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from HPHardDisk import *

class cpqDaPhyDrv(HPHardDisk):
    """cpqDaPhyDrv object
    """

    portal_type = meta_type = 'cpqDaPhyDrv'

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
		2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
		3: (DOT_RED, SEV_CRITICAL, 'Failed'),
		4: (DOT_ORANGE, SEV_ERROR, 'Predictive Failure'),
		}

InitializeClass(cpqDaPhyDrv)
