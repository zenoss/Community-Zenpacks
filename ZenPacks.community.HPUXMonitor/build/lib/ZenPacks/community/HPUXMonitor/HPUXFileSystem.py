################################################################################
#
# This program is part of the HPUXMonitor Zenpack for Zenoss.
# Copyright (C) 2008 Mike Albon & Zenoss Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """HPUXFileSystem

HPUXFileSystem is a variation on the existing FileSystem template provided with Zenoss Core

$Id: HPUXFileSystem.py,v 1.00 2008/10/03 16:56:00 mikea Exp $"""

__version__ = "$Revision: 1.00 $"[11:-2]


# Import existing FileSystem
from Products.ZenModel.FileSystem import *

class HPUXFileSystem(FileSystem):
    """
    HPUXFileSystem object
    """

    def availBlocks(self, default = None):
        """
        Return the number of available blocks stored in the filesystem's RRD file
        """
        blocks = self.cacheRRDValue('availBlocks', default)
        if blocks is not None:
            return long(blocks)
        return default

    def availBytes(self):
        blocks = self.availBlocks()
        if blocks is not None:
            return self.blockSize * blocks
        return None

    def usedBytes(self):
        avail = self.availBytes()
        if avail is not None:
            return self.totalBytes() - avail
        return None

    def getRRDNames(self):
        """
        Return the datapoint name of this filesystem 'availBlocks_availBlocks'
        """
        return ['availBlocks_availBlocks']


InitializeClass(HPUXFileSystem)

