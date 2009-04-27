################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqFcaLogDrv

cpqFcaLogDrv is an abstraction of a HP FCA Logical Disk.

$Id: cpqFcaLogDrv.py,v 1.0 2009/03/10 12:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from HPLogicalDisk import *

class cpqFcaLogDrv(HPLogicalDisk):
    """cpqFcaLogDrv object
    """

    portal_type = meta_type = 'cpqFcaLogDrv'

    chassis = ""
    external = False
    _properties = HPLogicalDisk._properties + (
                    {'id':'chassis', 'type':'string', 'mode':'w'},
                    {'id':'external', 'type':'boolean', 'mode':'w'},
                )    

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
		2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
		3: (DOT_RED, SEV_CRITICAL, 'Failed'),
		4: (DOT_YELLOW, SEV_WARNING, 'Unconfigured'),
		5: (DOT_ORANGE, SEV_ERROR, 'Recovering'),
		6: (DOT_YELLOW, SEV_WARNING, 'Ready Rebuild'),
		7: (DOT_YELLOW, SEV_WARNING, 'Rebuilding'),
		8: (DOT_ORANGE, SEV_ERROR, 'Wrong Drive'),
		9: (DOT_ORANGE, SEV_ERROR, 'Bad Connect'),
		10:(DOT_RED, SEV_CRITICAL, 'Overheating'),
		11:(DOT_RED, SEV_CRITICAL, 'Shutdown'),
		12:(DOT_YELLOW, SEV_WARNING, 'Expanding'),
		13:(DOT_YELLOW, SEV_WARNING, 'Not Available'),
		14:(DOT_YELLOW, SEV_WARNING, 'Queued For Expansion'),
		15:(DOT_RED, SEV_CRITICAL, 'Hard Error'),
		}

InitializeClass(cpqFcaLogDrv)
