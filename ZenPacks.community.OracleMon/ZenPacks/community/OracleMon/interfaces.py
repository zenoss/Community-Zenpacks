################################################################################
#
# This program is part of the OracleMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.0 2010/12/13 07:40:17 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t
from ZenPacks.community.RDBMS.interfaces import IDatabaseInfo, IDBSrvInstInfo


class IOracleDataSourceInfo(IInfo):
    name = schema.Text(title=_t(u'Name'))
    enabled = schema.Bool(title=_t(u'Enabled'))
    username = schema.Text(title=_t(u'Oracle Username'))
    password = schema.Text(title=_t(u'Oracle Password'))
    dsn = schema.Text(title=_t(u'Oracle TNS'))
    sql = schema.TextLine(title=_t(u'SQL Query'))
