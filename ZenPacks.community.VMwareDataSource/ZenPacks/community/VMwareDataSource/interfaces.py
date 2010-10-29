################################################################################
#
# This program is part of the VMwareDataSource Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IVMwareDataSourceInfo(IInfo):
	newId = schema.Text(title=_t(u'Name'),
						xtype="idfield",
						description=_t(u'The name of this datasource'))
	type = schema.Text(title=_t(u'Type'),
						readonly=True)
	enabled = schema.Bool(title=_t(u'Enabled'))
	severity = schema.Text(title=_t(u'Severity'), 
                           xtype='severity')
	eventKey = schema.Text(title=_t(u'Event Key'))
	eventClass = schema.Text(title=_t(u'Event Class'),
                             xtype='eventclass')
	component = schema.Text(title=_t(u'Component'))
	instance = schema.Text(title=_t(u'Instance'))
	performanceSource = schema.Text(title=_t(u'Performance Source'), group="Counter Group")
	instance = schema.Text(title=_t(u'Instance'), group="Counter Group")
