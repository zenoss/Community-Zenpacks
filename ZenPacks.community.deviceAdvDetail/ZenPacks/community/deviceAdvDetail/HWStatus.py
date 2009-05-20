################################################################################
#
# This program is part of the deviceAdvDetail Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HWStatus

HWStatus is an abstraction of Hardware status indication.

$Id: HWStatus.py,v 1.1 2009/05/21 00:26:24 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

DOT_GREEN    = 'green'
DOT_YELLOW   = 'yellow'
DOT_ORANGE   = 'orange'
DOT_RED      = 'red'
DOT_GREY     = 'grey'

SEV_CLEAN    = 0
SEV_DEBUG    = 1
SEV_INFO     = 2
SEV_WARNING  = 3
SEV_ERROR    = 4
SEV_CRITICAL = 5


class HWStatus:
    """HW Status object"""

    status = 1

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
	        2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
		3: (DOT_ORANGE, SEV_ERROR, 'Degraded'),
		4: (DOT_RED, SEV_CRITICAL, 'Failed'),
		}

    def statusDot(self, status=None):
        """
        Return the Dot Color based on maximal severity
        """
        colors = ['green', 'purple', 'blue', 'yellow', 'orange', 'red']
	if status: return self.statusmap.get(status, (DOT_GREY, SEV_WARNING, 'other'))[0]
	try:
	    return colors[self.ZenEventManager.getMaxSeverity(self)]
	except:
	    return 'grey' 

    def statusSeverity(self, status=None):
        """
        Return the severity based on status
	0:'Clean', 1:'Debug', 2:'Info', 3:'Warning', 4:'Error', 5:'Critical'
        """
	if not status: status = int(self.status)
	return self.statusmap.get(status, (DOT_GREY, SEV_WARNING, 'other'))[1]

    def statusString(self, status=None):
        """
        Return the status string
        """
	if not status: status = int(self.status)
	return self.statusmap.get(status, (DOT_GREY, SEV_WARNING, 'other'))[2]
