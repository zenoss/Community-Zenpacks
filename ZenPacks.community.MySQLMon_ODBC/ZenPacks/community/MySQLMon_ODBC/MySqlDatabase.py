################################################################################
#
# This program is part of the MySQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MySqlDatabase

MySqlDatabase is a Database

$Id: MySqlDatabase.py,v 1.1 2010/07/11 17:03:53 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass

from ZenPacks.community.RDBMS.Database import Database
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence


class MySqlDatabase(Database):
    """
    MySQL Database object
    """

    ZENPACKID = 'ZenPacks.community.MySQLMon_ODBC'

    def totalBytes(self):
        """
        Return the number of total bytes
        """
        su = self.cacheRRDValue('sizeUsed_sizeUsed', 0)
        return long(su) * long(self.blockSize)


InitializeClass(MySqlDatabase)
