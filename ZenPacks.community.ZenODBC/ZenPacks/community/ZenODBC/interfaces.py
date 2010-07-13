################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.0 2010/06/17 23:33:45 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IODBCDataSourceInfo(IInfo):
    name = schema.Text(title=_t(u'Name'))
    enabled = schema.Bool(title=_t(u'Enabled'))
    cs = schema.Text(title=_t(u'Connection String'))
    sql = schema.TextLine(title=_t(u'SQL Query'))

