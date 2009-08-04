################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMComponent

IBMComponent is an abstraction

$Id: IBMComponent.py,v 1.0 2009/07/13 00:09:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.HWStatus import *

class IBMComponent(HWStatus):

    statusmap ={0: (DOT_GREY, SEV_WARNING, 'Unknown'),
	        1: (DOT_GREY, SEV_WARNING, 'Other'),
	        2: (DOT_GREEN, SEV_CLEAN, 'OK'),
		3: (DOT_YELLOW, SEV_WARNING, 'Degraded'),
		4: (DOT_ORANGE, SEV_ERROR, 'Stressed'),
		5: (DOT_YELLOW, SEV_WARNING, 'Predictive Failure'),
		6: (DOT_ORANGE, SEV_ERROR, 'Error'),
		7: (DOT_RED, SEV_CRITICAL, 'Non-Recoverable Error'),
		8: (DOT_YELLOW, SEV_WARNING, 'Starting'),
		9: (DOT_YELLOW, SEV_WARNING, 'Stopping'),
		10: (DOT_YELLOW, SEV_WARNING, 'Stopped'),
		11: (DOT_YELLOW, SEV_WARNING, 'In Service'),
		12: (DOT_YELLOW, SEV_WARNING, 'No Contact'),
		13: (DOT_YELLOW, SEV_WARNING, 'Lost Communication'),
		14: (DOT_YELLOW, SEV_WARNING, 'Aborted'),
		15: (DOT_YELLOW, SEV_WARNING, 'Dormant'),
		16: (DOT_YELLOW, SEV_WARNING, 'Supporting Entity in Error'),
		17: (DOT_YELLOW, SEV_WARNING, 'Completed'),
		18: (DOT_YELLOW, SEV_WARNING, 'Power Mode'),
		}

