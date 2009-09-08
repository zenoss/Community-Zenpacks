################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OdbcClient

Gets ODBC performance data and stores it in RRD files.

$Id: OdbcClient.py,v 1.0 2009/08/14 23:42:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.Driver import drive
from Products.DataCollector.BaseClient import BaseClient

from twisted.enterprise import adbapi
from pyodbc import OperationalError, Error
from twisted.internet import threads, defer

import os
import socket
import sys
import logging
log = logging.getLogger("zen.OdbcClient")


class BadCredentials(Exception): pass

class CError:

    errormsg = ''
    
    def __init__(self, errormsg):
        self.errormsg = errormsg
        
    def getErrorMessage(self):
        return self.errormsg

class OdbcClient(BaseClient):

    def __init__(self, device, datacollector=None, plugins=[]):
        BaseClient.__init__(self, device, datacollector)
        self.device = device
        self.host = device.id
        if socket.getfqdn().lower() == device.id.lower(): 
            self.host = "."
        elif device.manageIp is not None:
            self.host = device.manageIp
        self.name = device.id
        self.datacollector = datacollector
        self.plugins = plugins
        self.results = []


    def query(self, queries):
        def _getQueries(txn, query):
            for q in query.split(';'):
                if not q.strip('\n '): continue
                txn.execute(q.strip('\n '))
            result = txn.fetchall()
            if result:
                return result
            else:
                return None
        def inner(driver):
            try:
                queryResult = {}
                dbpools = {}
                for table, query in queries.iteritems():
                    if not dbpools.has_key(query[0]):
                        dbpools[query[0]] = []
                    dbpools[query[0]].append((table, query[1], query[2]))
                for cs, qs in dbpools.iteritems():
                    dbpool = adbapi.ConnectionPool("pyodbc", cs,
                        autocommit=True, ansi=True, unicode_results=False)
                    for table, query, fields in qs:
                        queryResult[table] = []
                        try:
                            yield dbpool.runInteraction(_getQueries, query)
                            output = driver.next()
                            if not output: continue
                        except Error, ex:
                            queryResult[table] = [CError(str(ex))]
                            continue
                        try:
                            r = dict(output)
                            values = {}
                            for field in fields:
                                values[field] = r[field]
                            queryResult[table] = [values]
                        except:
                            for r in output:
                                queryResult[table].append(dict(zip(fields, r)))
                    dbpool.close()
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
