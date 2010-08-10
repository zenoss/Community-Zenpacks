################################################################################
#
# This program is part of the MsSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MsSql90Database

MsSql90Database is a MS SQL2005 Database

$Id: MsSql90Database.py,v 1.2 2010/08/10 22:36:37 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import InitializeClass

from ZenPacks.community.RDBMS.Database import Database
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence

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


class MsSql90Database(Database):
    """
    Database object
    """

    ZENPACKID = 'ZenPacks.community.MsSQLMon_ODBC'

    status = 0
    statusmap ={0: (DOT_GREEN, SEV_CLEAN, 'Online'),
                1: (DOT_RED, SEV_CRITICAL, 'Offline'),
                2: (DOT_YELLOW, SEV_WARNING, 'Restoring'),
                3: (DOT_YELLOW, SEV_WARNING, 'Recovering'),
                4: (DOT_ORANGE, SEV_ERROR, 'Recovery Pending'),
                5: (DOT_ORANGE, SEV_ERROR, 'Suspect'),
                6: (DOT_ORANGE, SEV_ERROR, 'Emergency'),
                }

    def totalBytes(self):
        """
        Return the number of allocated bytes
        """
        datasize = self.cacheRRDValue('databaseSize_dbSize', 0)
        logsize = self.cacheRRDValue('databaseSize_logSize', 0)
        sa = datasize + logsize
        if sa == 0: sa = self.totalBlocks
        return long(sa) * long(self.blockSize)

    def usedBytes(self):
        """
        Return the number of used bytes
        """
        reserved = self.cacheRRDValue('spaceUsed_reservedPages', 0)
        logsize = self.cacheRRDValue('databaseSize_logSize', 0)
        su = logsize + reserved
        return long(su) * long(self.blockSize)

InitializeClass(MsSql90Database)
