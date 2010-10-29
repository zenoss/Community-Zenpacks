###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
from Products.Zuul.interfaces import IBasicDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class ISplunkDataSourceInfo(IBasicDataSourceInfo):
    timeout = schema.Int(title=_t(u"Timeout (seconds)"))
    component = schema.Text(title=_t(u"Component"))
    eventKey = schema.Text(title=_t(u"Event Key"))
    
    splunkServer = schema.Text(title=_t(u"Splunk Server"),
                               group=_t('Splunk'))
    splunkUsername = schema.Text(title=_t(u"Splunk Username"),
                                 group=_t('Splunk'))
    splunkPort = schema.Int(title=_t(u"Splunk Port"),
                            group=_t('Splunk'))
    splunkPassword = schema.Password(title=_t(u"Splunk Password"),
                                     group=_t('Splunk'))
    splunkSearch = schema.Text(title=_t(u"Search"),
                               group=_t('Splunk'))
