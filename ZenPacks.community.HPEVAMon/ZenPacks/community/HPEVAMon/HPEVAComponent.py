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

$Id: HPEVAComponent.py,v 1.1 2010/05/21 09:10:43 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

class HPEVAComponent:

    def statusDot(self, status=None):
        """
        Return the Dot Color based on maximal severity
        """
        colors = {0:'green',1:'purple',2:'blue',3:'yellow',4:'orange',5:'red'}
        if not self.monitor: return 'grey'
        severity = self.ZenEventManager.getMaxSeverity(self)
        return colors.get(severity, 'grey')

    def statusString(self, status=None):
        """
        Return the status string
        """
        return self.state or 'Unknown'
