################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVADiskFCPort

HPEVADiskFCPort is an abstraction of a HPEVA_DiskFCPort

$Id: HPEVADiskFCPort.py,v 1.0 2010/05/10 15:23:54 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from HPEVAHostFCPort import *

class HPEVADiskFCPort(HPEVAHostFCPort):
    """DiskFCPort object"""

    portal_type = meta_type = 'HPEVADiskFCPort'


    def getStatus(self):
        """
        Return the components status
        """
        return int(round(self.cacheRRDValue('OperationalStatus', 0)))


InitializeClass(HPEVADiskFCPort)
