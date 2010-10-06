################################################################################
#
# This program is part of the MsSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of Databases.

$Id: info.py,v 1.1 2010/09/27 23:15:07 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from ZenPacks.community.RDBMS.info import DatabaseInfo, DBSrvInstInfo
from ZenPacks.community.MsSQLMon_ODBC import interfaces


class MsSqlDatabaseInfo(DatabaseInfo):
    implements(interfaces.IMsSqlDatabaseInfo)

    dbid = ProxyProperty("dbid")
    updateability = ProxyProperty("updateability")
    useraccess = ProxyProperty("useraccess")
    recovery = ProxyProperty("recovery")
    collation = ProxyProperty("collation")
    sqlsortorder = ProxyProperty("sqlsortorder")
    dbproperties = ProxyProperty("dbproperties")

class MsSqlSrvInstInfo(DBSrvInstInfo):
    implements(interfaces.IMsSqlSrvInstInfo)

    edition = ProxyProperty("edition")
    licenseType = ProxyProperty("licenseType")
    numLicenses = ProxyProperty("numLicenses")
    processID = ProxyProperty("processID")
    productVersion = ProxyProperty("productVersion")
    productLevel = ProxyProperty("productLevel")
    dbsiproperties = ProxyProperty("dbsiproperties")

