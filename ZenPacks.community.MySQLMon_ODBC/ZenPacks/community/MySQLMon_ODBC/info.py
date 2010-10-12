################################################################################
#
# This program is part of the MySQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of Data Source.

$Id: info.py,v 1.0 2010/10/06 10:28:52 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import InfoBase
from ZenPacks.community.RDBMS.info import DatabaseInfo, DBSrvInstInfo
from ZenPacks.community.MySQLMon_ODBC import interfaces


class MySQLDataSourceInfo(InfoBase):
    implements(interfaces.IMySQLDataSourceInfo)

    def __init__(self, dataSource):
        self._object = dataSource

    @property
    def id(self):
        return '/'.join(self._object.getPrimaryPath())

    @property
    def source(self):
        return self._object.getDescription()

    @property
    def type(self):
        return self._object.sourcetype

    enabled = ProxyProperty('enabled')
    hostname = ProxyProperty('hostname')
    port = ProxyProperty('port')
    username = ProxyProperty('username')
    password = ProxyProperty('password')
    dbname = ProxyProperty('dbname')
    sql = ProxyProperty('sql')

    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return True


class MySqlDatabaseInfo(DatabaseInfo):
    implements(interfaces.IMySqlDatabaseInfo)

    version = ProxyProperty("version")
    collation = ProxyProperty("collation")


class MySqlSrvInstInfo(DBSrvInstInfo):
    implements(interfaces.IMySqlSrvInstInfo)

    hostname = ProxyProperty("hostname")
    port = ProxyProperty("port")
    license = ProxyProperty("license")
    version = ProxyProperty("version")
    have = ProxyProperty("have")
