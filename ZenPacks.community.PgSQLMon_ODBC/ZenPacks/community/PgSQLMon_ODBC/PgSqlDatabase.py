################################################################################
#
# This program is part of the PgSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""PgSqlDatabase

PgSqlDatabase is a Database

$Id: PgSqlDatabase.py,v 1.1 2010/07/11 18:45:12 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass

from ZenPacks.community.RDBMS.Database import Database
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence


class PgSqlDatabase(Database):
    """
    Database object
    """

    ZENPACKID = 'ZenPacks.community.PgSQLMon_ODBC'

    status = 2

    def totalBytes(self):
        """
        Return the number of total bytes
        """
        su = self.cacheRRDValue('sizeUsed_sizeUsed', 0)
        return long(su) * long(self.blockSize)


InitializeClass(PgSqlDatabase)
