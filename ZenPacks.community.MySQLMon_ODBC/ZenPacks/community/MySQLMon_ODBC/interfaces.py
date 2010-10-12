################################################################################
#
# This program is part of the MySQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.2 2010/10/06 10:28:14 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t
from ZenPacks.community.RDBMS.interfaces import IDatabaseInfo, IDBSrvInstInfo


class IMySQLDataSourceInfo(IInfo):
    name = schema.Text(title=_t(u'Name'))
    enabled = schema.Bool(title=_t(u'Enabled'))
    hostname = schema.Text(title=_t(u'MySQL Host'))
    port = schema.Text(title=_t(u'MySQL Port'))
    username = schema.Text(title=_t(u'MySQL Username'))
    password = schema.Text(title=_t(u'MySQL Password'))
    dbname = schema.Text(title=_t(u'MySQL Database'))
    sql = schema.TextLine(title=_t(u'SQL Query'))


class IMySqlDatabaseInfo(IDatabaseInfo):
    """
    Info adapter for MySQL Database components.
    """
    activeTime = schema.Text(title=u"Created", readonly=True, group=u"Details")
    version = schema.Text(title=u"Version", readonly=True, group=u"Details")
    collation = schema.Text(title=u"Collation", readonly=True, group=u"Details")


class IMySqlSrvInstInfo(IDBSrvInstInfo):
    """
    Info adapter for MySQL Server Instance components.
    """
    hostname = schema.Text(title=u"Hostname", readonly=True, group=u"Details")
    port = schema.Text(title=u"Port", readonly=True, group=u"Details")
    version = schema.Text(title=u"Product Version", readonly=True, group=u"Details")
    license = schema.Text(title=u"License Type", readonly=True, group=u"Details")
    have = schema.List(title=u"Instance Properties", readonly=True, group=u"Details")
