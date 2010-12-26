################################################################################
#
# This program is part of the OracleMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of Data Source.

$Id: info.py,v 1.0 2010/12/13 07:38:11 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import InfoBase
from ZenPacks.community.RDBMS.info import DatabaseInfo, DBSrvInstInfo
from ZenPacks.community.OracleMon import interfaces


class OracleDataSourceInfo(InfoBase):
    implements(interfaces.IOracleDataSourceInfo)

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
    username = ProxyProperty('username')
    password = ProxyProperty('password')
    dsn = ProxyProperty('dsn')
    sql = ProxyProperty('sql')

    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return True
