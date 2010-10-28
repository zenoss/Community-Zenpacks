################################################################################
#
# This program is part of the FormulaDataSource Zenpack for Zenoss.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IFormulaDataSourceInfo(IInfo):
	newId = schema.Text(title=_t(u'Name'),
						xtype="idfield",
						description=_t(u'The name of this datasource'))
	type = schema.Text(title=_t(u'Type'),
						readonly=True)
	dataformula = schema.Text(title=_t(u'Data Formula'))
	enabled = schema.Bool(title=_t(u'Enabled'))
