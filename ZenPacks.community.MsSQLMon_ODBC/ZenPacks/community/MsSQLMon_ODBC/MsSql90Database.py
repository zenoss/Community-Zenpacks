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

$Id: MsSql90Database.py,v 1.3 2010/08/10 22:36:37 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Globals import InitializeClass
from MsSqlDatabase import MsSqlDatabase

class MsSql90Database(MsSqlDatabase):
    """
    Database object
    """
    pass

InitializeClass(MsSql90Database)
