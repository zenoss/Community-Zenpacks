################################################################################
#
# This program is part of the SQLDataSource Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SQLClient

Gets performance data over python DB API.

$Id: SQLClient.py,v 1.0 2010/06/14 08:58:46 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

import Globals
from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.Driver import drive
from Products.DataCollector.BaseClient import BaseClient

from twisted.enterprise import adbapi
from twisted.internet import defer, reactor
from twisted.python.failure import Failure

import datetime
import decimal
from DateTime import DateTime

import os
import sys
import logging
log = logging.getLogger("zen.SQLClient")

BaseName = os.path.basename(sys.argv[0])
MyName = None


def _myname():
    global MyName
    if not MyName:
        MyName = BaseName.split('.')[0]
        try:
            os.mkdir(zenPath('var', _myname()))
        except os.error:
            pass
    return MyName

def _filename(device):
    return zenPath('var', _myname(), device)


def sortQuery(qs, table, query):
    sql, kbs, cs, cols = query
    if not kbs: kbs = {}
    ikey = tuple(kbs.keys())
    ival = tuple(kbs.values())
    try:
        if ival not in qs[cs][sql][ikey]:
            qs[cs][sql][ikey][ival] = []
        qs[cs][sql][ikey][ival].append((table, cols))
    except KeyError:
        try:
            qs[cs][sql][ikey] = {}
        except KeyError:
            try:
                qs[cs][sql] = {}
            except KeyError:
                qs[cs] = {}
                qs[cs][sql] = {}
            qs[cs][sql][ikey] = {}
        qs[cs][sql][ikey][ival] = [(table, cols)]
    return qs


class BadCredentials(Exception): pass


class SQLClient(BaseClient):

    def __init__(self, device=None, datacollector=None, plugins=[]):
        BaseClient.__init__(self, device, datacollector)
        self.device = device
        self.datacollector = datacollector
        self.plugins = plugins
        self.results = []


    def parseError(self, err, query, resMaps):
        err = Failure(err)
        err.value = 'Received error (%s) from query: %s'%(err.value, query)
        log.error(err.getErrorMessage())
        results = {}
        for instances in resMaps.values():
            for tables in instances.values():
                for table, props in tables:
                    results[table] = [err,]
        return results


    def parseValue(self, value):
        if isinstance(value, datetime.datetime): return DateTime(value)
        if isinstance(value, decimal.Decimal): return int(value)
        try: return int(value)
        except: pass
        try: return float(value)
        except: pass
        try: return DateTime(value)
        except: return value


    def parseResults(self, rows, resMaps):
        results = {}
        try:
            header = [h[0] for h in rows[0]]
            rows = rows[1]
        except: return results
        try: rdict = dict(rows)
        except: rdict = None
        for maps in resMaps.values():
            for tables in maps.values():
                for table, cols in tables:
                    results[table] = []
                    if not rdict: continue
                    try:
                        result = {}
                        for name, anames in cols.iteritems():
                            if type(anames) is not tuple: anames = (anames,)
                            for aname in anames:result[aname] = self.parseValue(
                                                                    rdict[name])
                        if result: results[table].append(result)
                    except: rdict = None
        if rdict: return results
        for row in rows:
            for kbKey, kbVal in resMaps.iteritems():
                if kbKey == (): kbIns = ()
                else: kbIns = row[(0 - len(kbKey)):]
                for tkey, tables in kbVal.iteritems():
                    if tuple([str(t.strip('"\' ')) for t in tkey]) != kbIns:
                        continue
                    for table, cols in tables:
                        result = {}
                        current_row = list(row[:])
                        clist = cols.keys()
                        clist.sort()
                        for name in clist:
                            anames = cols[name]
                            try: valindex = header.index(name)
                            except: valindex = clist.index(name)
                            res = self.parseValue(current_row[valindex])
                            if type(anames) is not tuple: anames = (anames,)
                            for aname in anames:result[aname] = res
                        if result: results[table].append(result)
#                    del kbVal[tkey]
                    break
        return results


    def parseCS(self, cs):
        args = []
        kw = {}
        for arg in cs.split(','):
            try:
                if arg.strip().startswith("'"):
                    arg = arg.strip("' ")
                    raise
                var, val = arg.strip().split('=', 1)
                if val.startswith('\'') or val.startswith('"'):
                    kw[var.strip()] = val.strip('\'" ')
                else:
                    kw[var.strip()] = int(val.strip())
            except: args.append(arg)
        return args, kw


    def query(self, queries):
        resMaps = {}
        for table, query in queries.iteritems():
            resMaps = sortQuery(resMaps, table, query)
        return self.sortedQuery(resMaps)


    def sortedQuery(self, queries):
        def _getQueries(txn, query):
            for q in query.split(';'):
                if not q.strip('\n '): continue
                txn.execute(q.strip('\n '))
            return txn.description, txn.fetchall()

        def inner(driver):
            try:
                queryResult = {}
                for cs, qs in queries.iteritems():
                    args, kw = self.parseCS(cs)
                    dbpool = adbapi.ConnectionPool(*args, **kw)
                    for query, resMaps in qs.iteritems():
                        if () not in resMaps:
                            if len(resMaps.values()[0].values()) > 1: kb = ''
                            else:
                                if query.upper().__contains__('WHERE %s'):
                                    kb = 'AND '
                                else: kb = 'WHERE '
                                kb += ' AND '.join(
                                    ['='.join(k) for k in zip(resMaps.keys()[0],
                                    resMaps.values()[0].keys()[0])])
                            query = query%kb
                        try:
                            yield dbpool.runInteraction(_getQueries, query)
                            queryResult.update(self.parseResults(driver.next(),
                                                                    resMaps))
                        except StandardError, ex:
                            queryResult.update(self.parseError(ex, query,
                                                                    resMaps))
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
                for plugin in self.plugins:
                    pluginName = plugin.name()
                    log.debug("Sending queries for plugin: %s", pluginName)
                    log.debug("Queries: %s" % str(plugin.queries(self.device)))
                    try:
                        yield self.query(plugin.queries(self.device))
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

def SQLGet(cs, query, columns):
    from SQLPlugin import SQLPlugin
    sp = SQLPlugin()
    sp.tables = {'t': (query, {}, cs, columns)}
    cl = SQLClient(device=None, plugins=[sp,])
    cl.run()
    reactor.run()
    for plugin, result in cl.getResults():
        if plugin == sp and 't' in result:
            return result['t']
    return result


if __name__ == "__main__":
    cs = "MySQLdb,host='127.0.0.1',port=3307,db='information_schema',user='zenoss',passwd='zenoss'"
    query = "USE information_schema; SHOW GLOBAL STATUS;"
    columns = ["Bytes_received", "Bytes_sent"]
    aliases = ["Bytes_received", "Bytes_sent"]
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:q:f:a:",
                    ["help", "cs=", "query=", "fields=", "aliases="])
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
            columns = arg.split()
        elif opt in ("-a", "--aliases"):
            aliases = arg.split()
    columns = dict(zip(columns, aliases))
    results = SQLGet(cs, query, columns)
    if type(results) is not list:
        print results
        sys.exit(1)
    if len(results) > 1 and not isinstance(results[0], Failure):
        print "|".join(results[0].keys())
    for res in results:
        if isinstance(res, Failure):
            print res.getErrorMessage()
        else:
            if len(results) == 1:
                for var, val in res.items():
                    if var in columns.values():
                        var = columns.keys()[columns.values().index(var)]
                    print "%s = %s"%(var, val)
            else: print "|".join([str(r) for r in res.values()])
