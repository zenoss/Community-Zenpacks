################################################################################
#
# This program is part of the NWMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
# Based on HPUXFileSystem.py from Mike Albon & Zenoss Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """NWFileSystem

NWFileSystem is a variation on the existing FileSystem template provided with
Zenoss Core

$Id: NWFileSystem.py,v 1.1 2010/04/23 14:05:010 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]


from Products.ZenModel.FileSystem import *

class NWFileSystem(FileSystem):
    """
    NWFileSystem object
    """

    def availBlocks(self):
        blocks = self.availBytes() / self.blockSize
        if blocks is not None:
            return long(blocks)
        return None

    def availBytes(self, default = None):
        """
        Return the number of available bytes stored in the filesystem's RRD file
        """
        avail = self.cacheRRDValue('availKBytes', default)
        if avail is not None:
            return long(avail) * 1024
        return None

    def usedBytes(self, default = None):
        """
        Return the number of used bytes
        """
        avail = self.availBytes()
        freeable = self.cacheRRDValue('freeableKBytes', default)
        nonfreeable = self.cacheRRDValue('nonFreeableKBytes', default)
        if avail is not None:
            used = self.totalBytes() - avail
            if nonfreeable is not None:
                used = used - (long(nonfreeable) * 1024)
            if freeable is not None:
                used = used - (long(freeable) * 1024)
            return used
        return None

    def availFiles(self):
        try:
            avail = self.totalFiles - self.usedFiles()
            return long(avail)
        except:
            return None

    def usedFiles(self, default = None):
        """
        Return the number of Directory Entries used
        """
        used = self.cacheRRDValue('usedFiles', default)
        if used is not None:
            return long(used)
        return None

    def getRRDNames(self):
        """
        Return the datapoint name of this filesystem 'availKBytes_availKBytes',
        'freeableKBytes_freeableKBytes', 'nonFreeableKBytes_nonFreeableKBytes',
        'usedFiles_usedFiles'
        """
        return ['availKBytes_availKBytes',
                'freeableKBytes_freeableKBytes',
                'nonFreeableKBytes_nonFreeableKBytes',
                'usedFiles_usedFiles',
                ]


InitializeClass(NWFileSystem)

