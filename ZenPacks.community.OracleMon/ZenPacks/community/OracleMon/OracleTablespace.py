################################################################################
#
# This program is part of the OracleMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OracleDatabase

OracleDatabase is a Database

$Id: OracleDatabase.py,v 1.2 2010/10/05 21:20:30 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.RDBMS.Database import Database


class OracleTablespace(Database):
    """
    Oracel Tablespace object
    """

    ZENPACKID = 'ZenPacks.community.OracleMon'


    statusmap ={1: ('grey', 3, 'Unknown'),
                2: ('green', 0, 'ONLINE'),
                3: ('yellow',3 ,'Available'),
                4: ('orange', 4, 'OFFLINE'),
                5: ('red', 5, 'INVALID'),
                }


    def totalBytes(self):
        """
        Return the number of total bytes
        """
        return self.cacheRRDValue('sizeUsed_totalBytes', 0)


    def dsn(self):
        """
        Return the DSN string
        """
        inst = self.getDBSrvInst()
        return getattr(inst, 'dsn', '')

InitializeClass(OracleTablespace)
