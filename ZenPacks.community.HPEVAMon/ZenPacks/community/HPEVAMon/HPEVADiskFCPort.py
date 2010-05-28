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

$Id: HPEVADiskFCPort.py,v 1.1 2010/05/18 13:35:52 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from HPEVAHostFCPort import *

class HPEVADiskFCPort(HPEVAHostFCPort):
    """DiskFCPort object"""

    portal_type = meta_type = 'HPEVADiskFCPort'

InitializeClass(HPEVADiskFCPort)
