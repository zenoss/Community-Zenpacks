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
from Products.Zuul.infos import ProxyProperty
from zope.interface import implements
from Products.Zuul.infos.template import BasicDataSourceInfo
from ZenPacks.community.Splunk.interfaces import ISplunkDataSourceInfo


class SplunkDataSourceInfo(BasicDataSourceInfo):
    implements(ISplunkDataSourceInfo)
    component = ProxyProperty('component')
    eventKey = ProxyProperty('eventKey')
    timeout = ProxyProperty('timeout')
    splunkServer = ProxyProperty('splunkServer')
    splunkPort = ProxyProperty('splunkPort')
    splunkUsername = ProxyProperty('splunkUsername')
    splunkPassword = ProxyProperty('splunkPassword')
    splunkSearch = ProxyProperty('splunkSearch')
    
    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
    


