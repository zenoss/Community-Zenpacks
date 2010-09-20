################################################################################
#
# This program is part of the MsSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MsSql80Database

MsSql80Database is a MS SQL 2000 Database

$Id: MsSql80Database.py,v 1.3 2010/08/26 16:11:16 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Globals import InitializeClass
from MsSqlDatabase import MsSqlDatabase

class MsSql80Database(MsSqlDatabase):
    """
    Database object
    """
    pass

InitializeClass(MsSql80Database)
