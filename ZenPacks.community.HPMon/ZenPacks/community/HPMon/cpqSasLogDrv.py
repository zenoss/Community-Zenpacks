################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqSasLogDrv

cpqSasLogDrv is an abstraction of a HP SAS Logical Disk.

$Id: cpqSasLogDrv.py,v 1.0 2009/03/10 12:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from HPLogicalDisk import *

class cpqSasLogDrv(HPLogicalDisk):
    """cpqSasLogDrv object
    """

    portal_type = meta_type = 'cpqSasLogDrv'

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
		2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
		3: (DOT_ORANGE, SEV_ERROR, 'Degraded'),
		4: (DOT_YELLOW, SEV_WARNING, 'Rebuilding'),
		5: (DOT_RED, SEV_CRITICAL, 'Failed'),
		6: (DOT_ORANGE, SEV_ERROR, 'Offline'),
		}

InitializeClass(cpqSasLogDrv)
