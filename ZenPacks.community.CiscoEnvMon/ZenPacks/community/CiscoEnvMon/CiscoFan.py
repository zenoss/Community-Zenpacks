################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CiscoFan

CiscoFan is an abstraction of a Fan.

$Id: CiscoFan.py,v 1.0 2010/12/13 19:57:49 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.Fan import Fan

class CiscoFan(Fan):
    """Cisco Fan object"""

    portal_type = meta_type = 'CiscoFan'

    def rpmString(self):
        return self.state

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

InitializeClass(CiscoFan)
