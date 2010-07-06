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

$Id: HPEVADiskFCPort.py,v 1.2 2010/06/30 17:08:21 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from HPEVAHostFCPort import *

class HPEVADiskFCPort(HPEVAHostFCPort):
    """DiskFCPort object"""

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(HPEVADiskFCPort)
