################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAComponent

HPEVAComponent is an abstraction .

$Id: HPEVAComponent.py,v 1.0 2010/03/09 16:32:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

DOT_GREEN    = 'green'
DOT_PURPLE   = 'purple'
DOT_BLUE     = 'blue'
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

class HPEVAComponent:

    statusmap ={0: (DOT_GREY, SEV_WARNING, 'Unknown'),
                1: (DOT_GREY, SEV_WARNING, 'Other'),
	        2: (DOT_GREEN, SEV_CLEAN, 'OK'),
		3: (DOT_ORANGE, SEV_ERROR, 'Degraded'),
		4: (DOT_YELLOW, SEV_WARNING, 'Stressed'),
		5: (DOT_YELLOW, SEV_WARNING, 'Predictive Failure'),
		6: (DOT_ORANGE, SEV_ERROR, 'Error'),
		7: (DOT_RED, SEV_CRITICAL, 'Non-Recoverable Error'),
		8: (DOT_BLUE, SEV_INFO, 'Starting'),
		9: (DOT_YELLOW, SEV_WARNING, 'Stopping'),
		10: (DOT_ORANGE, SEV_ERROR, 'Stopped'),
		11: (DOT_BLUE, SEV_INFO, 'In Service'),
		12: (DOT_GREY, SEV_WARNING, 'No Contact'),
		13: (DOT_ORANGE, SEV_ERROR, 'Lost Communication'),
		14: (DOT_ORANGE, SEV_ERROR, 'Aborted'),
		15: (DOT_GREY, SEV_WARNING, 'Dormant'),
		16: (DOT_ORANGE, SEV_ERROR, 'Stopping Entity in Error'),
		17: (DOT_GREEN, SEV_CLEAN, 'Completed'),
		18: (DOT_YELLOW, SEV_WARNING, 'Power Mode'),
		}

#    def getStatus(self):
#        """
#        Return the components status
#	"""
#        return round(self.cacheRRDValue('OperationalStatus', 0))

    def statusDot(self, status=None):
        """
        Return the Dot Color based on maximal severity
        """
	if status is None:
            colors=['grey', 'green', 'purple', 'blue', 'yellow','orange', 'red']
            if not self.monitor: return DOT_GREY
	    status = self.getStatus()
	    severity = colors.index(self.statusmap[status][0])
            eseverity = self.ZenEventManager.getMaxSeverity(self) + 1
            if severity == 0 and eseverity == 1: return DOT_GREY
            if eseverity > severity:
                severity = eseverity
	    return colors[severity]
	return self.statusmap.get(status, (DOT_GREY, SEV_WARNING, 'other'))[0]

    def statusSeverity(self, status=None):
        """
        Return the severity based on status
	0:'Clean', 1:'Debug', 2:'Info', 3:'Warning', 4:'Error', 5:'Critical'
        """
	if status is None: status = self.getStatus()
	return self.statusmap.get(status, (DOT_GREY, SEV_WARNING, 'other'))[1]

    def statusString(self, status=None):
        """
        Return the status string
        """
	if status is None: status = self.getStatus()
	return self.statusmap.get(status, (DOT_GREY, SEV_WARNING, 'other'))[2]
