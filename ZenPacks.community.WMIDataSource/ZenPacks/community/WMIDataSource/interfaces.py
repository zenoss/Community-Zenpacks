################################################################################
#
# This program is part of the WMIDataSource Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.1 2010/06/13 16:36:29 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IWMIDataSourceInfo(IInfo):
    name = schema.Text(title=_t(u'Name'))
    enabled = schema.Bool(title=_t(u'Enabled'))
    namespace = schema.Text(title=_t(u'Namespace'))
    wql = schema.TextLine(title=_t(u'Query'))

