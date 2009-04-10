################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPComponent

HPComponent is an abstraction .

$Id: HPComponent.py,v 1.0 2009/03/10 15:32:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

class HPComponent:
    """HP object"""

    status = 1

    statusmap = [(4, 3, 'other'),
	        (4, 3, 'other'),
	        (0, 0, 'Ok'),
		(2, 4, 'Degraded'),
		(3, 5, 'Failed'),
		]

    def statusDot(self, status=None):
        """
        Return the Dot Color based on status
	0:'green', 1:'yellow', 2:'orange', 3:'red', 4:'grey'
        """
	try:
	    return self.statusmap[int(self.status)][0]
	except:
	    return 4

    def statusSeverity(self, status=None):
        """
        Return the severity based on status
	0:'Clean', 1:'Debug', 2:'Info', 3:'Warning', 4:'Error', 5:'Critical'
        """
	try:
	    return self.statusmap[int(self.status)][1]
	except:
	    return 3

    def statusString(self, status=None):
        """
        Return the status string
        """
	try:
	    return self.statusmap[int(self.status)][2]
	except:
	    return 'other'
