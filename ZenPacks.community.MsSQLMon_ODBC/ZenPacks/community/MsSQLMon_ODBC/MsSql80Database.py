################################################################################
#
# This program is part of the MsSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MsSql80Database

MsSql80Database is a MS SQL 2000 Database

$Id: MsSql80Database.py,v 1.0 2009/05/20 15:00:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]
from Globals import InitializeClass

from ZenPacks.community.deviceAdvDetail.HWStatus import *
from ZenPacks.community.RDBMS.Database import Database
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence


class MsSql80Database(Database, HWStatus):
    """
    Database object
    """

    ZENPACKID = 'ZenPacks.community.MsSQLMon_ODBC'

    portal_type = meta_type = 'MsSql80Database'
    
    __status = 0
    statusmap ={0: (DOT_GREEN, SEV_CLEAN, 'Online'),
		1: (DOT_RED, SEV_CRITICAL, 'Offline'),
		2: (DOT_YELLOW, SEV_WARNING, 'Restoring'),
		3: (DOT_YELLOW, SEV_WARNING, 'Recovering'),
		4: (DOT_ORANGE, SEV_ERROR, 'Recovery Pending'),
		5: (DOT_ORANGE, SEV_ERROR, 'Suspect'),
		6: (DOT_ORANGE, SEV_ERROR, 'Emergency'),
		}
    
    def _setStatus(self, state):
	if (state & 512):
	    self.__status = 1
	elif (state & 32):
	    self.__status = 2
	elif (state & 64):
	    self.__statue = 3
	elif (state & 128):
	    self.__statue = 4
	elif (state & 256):
	    self.__statue = 5
	elif (state & 32768):
	    self.__statue = 6
	else:
	    self.__status = 0
	    
    def _getStatus(self):
        return self.__status

    status = property(fget=lambda self: self._getStatus(),
                      fset=lambda self, v: self._setStatus(v)
		      )        

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

    
InitializeClass(MsSql80Database)
