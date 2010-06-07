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

$Id: interfaces.py,v 1.0 2010/05/31 19:01:22 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IWMIDataSourceInfo(IInfo):
    name = schema.Text(title=_t(u'Name'))
    enabled = schema.Bool(title=_t(u'Enabled'))
    namespace = schema.Text(title=_t(u'CIM Namespace'))
    wql = schema.TextLine(title=_t(u'WQL Queue'))
    
    
    

