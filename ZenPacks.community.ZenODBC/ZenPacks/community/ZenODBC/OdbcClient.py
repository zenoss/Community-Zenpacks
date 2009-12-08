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

$Id: OdbcClient.py,v 1.4 2009/12/08 22:45:23 egor Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

import Globals
from Products.ZenUtils.Driver import drive
from Products.DataCollector.BaseClient import BaseClient

from twisted.internet import defer, reactor

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

class pyOdbcClient:

    def __init__(self, connectionString):
        self.results = {}
        self.connectionString = connectionString
        self.dbpool = adbapi.ConnectionPool("pyodbc", connectionString,
                            autocommit=True, ansi=True, unicode_results=False)

    def addResult(self, result, table):
        self.results[table] = result
            
    def addError(self, ex, table):
        log.debug("Exception collecting query: %s\n", str(ex.value[1]))
        self.results[table] = [CError(str(ex.value[1]))]

    def getResults(self, results):
        self.dbpool.close()
        return self.results

    def query(self, queries):
        def _getQueries(txn, query, fields):
            for q in query.split(';'):
                if not q.strip('\n '): continue
                txn.execute(q.strip('\n '))
            result = txn.fetchall()
            if result:
                try:
                    r = dict(result)
                    values = {}
                    for field in fields:
                        values[field] = r[field]
                    table = [values]
                except:
                    table = []
                    for r in result:
                        table.append(dict(zip(fields, r)))
                return table
            else:
                return None
            
        deferreds = []
        for table, query, fields in queries:
            deferreds.append(self.dbpool.runInteraction(_getQueries, query,
                                                                    fields))
            deferreds[-1].addCallback(self.addResult, table)
            deferreds[-1].addErrback(self.addError, table)
        dl = defer.DeferredList(deferreds)
        dl.addCallback(self.getResults)
        return dl

try:
    from twisted.enterprise import adbapi
    from pyodbc import OperationalError, Error
    currentOdbcClient = pyOdbcClient
except:
    from isqlClient import isqlClient
    currentOdbcClient = isqlClient

class OdbcClient(BaseClient):

    def __init__(self, device=None, datacollector=None, plugins=[]):
        BaseClient.__init__(self, device, datacollector)
        self.device = device
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
                    odbcc = currentOdbcClient(cs)
                    yield odbcc.query(qs)
                    queryResult.update(driver.next()) 
                yield defer.succeed(queryResult)
                driver.next()
            except Exception, ex:
                log.debug("Exception collecting query: %s", str(ex))
                raise
        return drive(inner)

    def run(self):
        def inner(driver):
            try:
                for plugin in self.plugins:
                    pluginName = plugin.name()
                    log.debug("Sending queries for plugin: %s", pluginName)
                    log.debug("Queries: %s" % str(plugin.queries(self.device)))
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
            else:
                reactor.stop()
        d.addBoth(finish)
        return d


    def getResults(self):
        """Return data for this client
        """
        return self.results


def OdbcGet(tables):
    from OdbcPlugin import OdbcPlugin
    op = OdbcPlugin()
    op.tables = tables
    cl = OdbcClient(plugins=[op,])
    cl.run()
    reactor.run()
    try:
        return cl.getResults()[0][1]
    except:
        return


if __name__ == "__main__":
    cs = "DRIVER={MySQL};OPTION=3;PORT=3306;Database=information_schema;SERVER=localhost;UID=zenoss;PWD=zenoss"
    query = "USE information_schema; SHOW GLOBAL STATUS;"
    fields = ['Bytes_received', 'Bytes_sent']
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:q:f:",
                        ["help", "cs=", "query=", "fields="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-c", "--cs"):
            cs = arg
        elif opt in ("-q", "--query"):
            query = arg
        elif opt in ("-f", "--fields"):
            fields = arg.split()
    res = OdbcGet({'t': (cs, query, fields)})['t'][0]
    if isinstance(res, CError):
        print res.getErrorMessage()
    else:
        for var, val in res.items():
            print "%s = %s"%(var, val)
