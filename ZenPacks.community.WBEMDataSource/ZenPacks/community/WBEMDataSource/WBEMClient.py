################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WBEMClient

Gets WBEM performance data.

$Id: WBEMClient.py,v 1.0 2009/07/25 00:35:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.Driver import drive
from Products.DataCollector.BaseClient import BaseClient

from ZenPacks.community.WBEMDataSource.lib import pywbem

from twisted.internet import threads, defer

import os
import socket
import sys
import logging
log = logging.getLogger("zen.WBEMClient")


class BadCredentials(Exception): pass

class WBEMClient(BaseClient):

    def __init__(self, device, datacollector=None, plugins=[]):
        BaseClient.__init__(self, device, datacollector)
        self.device = device
        self.host = device.id
        if socket.getfqdn().lower() == device.id.lower(): 
            self.host = "."
            device.zWinUser = device.zWinPassword = ""
        elif device.manageIp is not None:
            self.host = device.manageIp
        self.name = device.id
        self.url = 'http%s://%s:%s' % (device.zWbemUseSSL is True and 's' or '',
                                                    self.host, device.zWbemPort)
        self.creds = (device.zWinUser, device.zWinPassword)
        self._wbem = pywbem.WBEMConnection(self.url, self.creds, 
                                            default_namespace='root/cimv2')
        self.datacollector = datacollector
        self.plugins = plugins
        self.results = []


    def query(self, queries):
        def inner(driver):
            try:
                queryResult = {}
                for tableName, query in queries.items():
                    if query[1]:
                        instancename = pywbem.CIMInstanceName(query[0],
                                                    keybindings=query[1],
                                                    namespace=query[2])
                        queryResult[tableName] = self._wbem.GetInstance(
                                                        instancename,
                                                        PropertyList=query[3])
                    else:
                        queryResult[tableName] = self._wbem.EnumerateInstances(
                                                        query[0])
                yield defer.succeed(queryResult)
                driver.next()
            except Exception, ex:
                log.debug("Exception collecting query: %s", str(ex))
                raise
        return drive(inner)

    def run(self):
        def inner(driver):
            try:
                driver.next()
                for plugin in self.plugins:
                    pluginName = plugin.name()
                    log.debug("Sending queries for plugin: %s", pluginName)
                    log.debug("Queries: %s" % str(plugin.queries().values()))
                    try:
                        yield self.query(plugin.queries())
                        self.results.append((plugin, driver.next()))
                    except Exception, ex:
                        self.results.append((plugin, ex))
            except Exception, ex:
                raise
        d = drive(inner)
        def finish(result):
            if self.datacollector:
                self.datacollector.clientFinished(self)
        d.addBoth(finish)
        return d


    def getResults(self):
        """Return data for this client
        """
        return self.results
