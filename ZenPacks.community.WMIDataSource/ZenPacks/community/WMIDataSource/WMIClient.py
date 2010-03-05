################################################################################
#
# This program is part of the WMIDataSource Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WMIClient

Gets WMI performance data.

$Id: WMIClient.py,v 1.5 2010/03/04 13:53:15 egor Exp $"""

__version__ = "$Revision: 1.5 $"[11:-2]

if __name__ == "__main__":
    import pysamba.twisted.reactor
from pysamba.twisted.callback import WMIFailure
from Query import Query

from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.Driver import drive
from Products.DataCollector.BaseClient import BaseClient
from ZenPacks.community.WMIDataSource.services.WmiPerfConfig import sortQuery

from twisted.internet import defer, reactor
from datetime import datetime, timedelta, tzinfo

import os
import socket
import sys
import logging
log = logging.getLogger("zen.WMIClient")

import re
DTPAT=re.compile(r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})\.(\d{6})([+|-])(\d{3})')


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

class MinutesFromUTC(tzinfo):
    """Fixed offset in minutes from UTC."""
    def __init__(self, offset):
        self.__offset = timedelta(minutes = offset)
    def utcoffset(self, dt):
        return self.__offset
    def dst(self, dt):
        return timedelta(0)

class BadCredentials(Exception): pass

class CError:

    errormsg = ''

    def __init__(self, errormsg):
        self.errormsg = errormsg

    def getErrorMessage(self):
        return self.errormsg

class WMIClient(BaseClient):

    def __init__(self, device, datacollector=None, plugins=[]):
        BaseClient.__init__(self, device, datacollector)
        self.device = device
        self.host = device.id
        self._wmipool = {}
        if device.zWmiProxy is not "":
            self.host = device.zWmiProxy
        elif socket.getfqdn().lower() == device.id.lower(): 
            self.host = "."
            device.zWinUser = device.zWinPassword = ""
        elif device.manageIp is not None:
            self.host = device.manageIp
        self.name = device.id
        self.user = device.zWinUser
        self.passwd = device.zWinPassword
        self.datacollector = datacollector
        self.plugins = plugins
        self.results = []


    def connect(self, namespace="root\\cimv2"):
        from pysamba.twisted.reactor import eventContext
        log.debug("connect to %s, user %r", self.host, self.user)
        if not self.user:
            log.warning("Windows login name is unset: "
                        "please specify zWinUser and "
                        "zWinPassword zProperties before adding devices.")
            raise BadCredentials("Username is empty")
        self._wmipool[namespace] = Query()
        creds = '%s%%%s' % (self.user, self.passwd)
        return self._wmipool[namespace].connect(eventContext, self.device.id,
                                                self.host, creds, namespace)


    def close(self, namespace=None):
        if not namespace:
            namespaces = self._wmipool.keys()
        else:
            namespaces = [namespace]
        for namespace in namespaces:
            self._wmipool[namespace].close()
            del self._wmipool[namespace]


    def parseError(self, err, query, instMap):
        msg = 'Received %s from query: %s'%(err, query)
        err = CError(msg)
        log.error(msg)
        results = {}
        for instances in instMap.values():
            for tables in instances.values():
                for table, props in tables:
                    results[table] = [err]
        return results


    def parseResults(self, instances, instMap):
        results = {}
        for instance in instances:
            for kbKey, kbVal in instMap.iteritems():
                kbIns = []
                if kbKey != ():
                    for k in kbKey:
                        val = getattr(instance, k.lower(), None)
                        if type(val) is str:
                            kbIns.append('"%s"'%val)
                        else:
                            kbIns.append(str(val))
                    if tuple(kbIns) not in kbVal: continue
                lastprops = None
                for table, properties in kbVal[tuple(kbIns)]:
                    if properties == lastprops and lastprops is not None:
                        results[table].append(result)
                        continue
                    result = {}
                    if len(properties) == 0:
                        properties = instance.__dict__.keys()
                    if type(properties) is not dict:
                        properties = dict(zip(properties, properties))
                    for name, aname in properties.iteritems():
                        if name is '_class_name': continue
                        result[aname] = getattr(instance, name.lower(), None)
                        if type(result[aname]) is not str: continue
                        r = DTPAT.search(result[aname])
                        if not r: continue
                        g = r.groups()
                        result[aname] = datetime(int(g[0]), int(g[1]), 
                                    int(g[2]), int(g[3]), 
                                    int(g[4]), int(g[5]), 
                                    int(g[6]), MinutesFromUTC(int(g[7]+g[8])))
                    if table not in results:
                        results[table] = []
                    results[table].append(result)
        return results


    def query(self, queries, includeQualifiers=True):
        instMap = {}
        for table, query in queries.iteritems():
            instMap = sortQuery(instMap, table, query)
        return self.sortedQuery(instMap, includeQualifiers=includeQualifiers)


    def sortedQuery(self, queries, includeQualifiers=False):
        def inner(driver):
            try:
                queryResult = {}
                for namespace, classes in queries.iteritems():
                    yield self.connect(namespace=namespace)
                    driver.next()
                    for classname, instMap in classes.iteritems():
                        if classname.upper().startswith('SELECT '):
                            query = classname
                        elif () in instMap or len(instMap.values()[0]) > 1:
                            query = "SELECT * FROM %s"%classname
                        else:
                            kb = zip(instMap.keys()[0],
                                    instMap.values()[0].keys()[0])
                            query = "SELECT * FROM %s WHERE %s"%(classname,
                                    " AND ".join(['%s=%s'%v for v in kb]))
                        query = query.replace ("\\", "\\\\")
                        log.debug("Query: %s", query)
                        yield self._wmipool[namespace].query(query)
                        result = driver.next()
                        instances = []
                        while 1:
                            more = None
                            yield result.fetchSome(includeQualifiers=includeQualifiers)
                            try:
                                more = driver.next()
                            except WMIFailure, ex:
                                queryResult.update(self.parseError(ex, query,
                                                                    instMap))
                                break
                            if not more:
                                queryResult.update(self.parseResults(instances,
                                                                    instMap))
                                break
                            instances.extend(more)
                    self.close(namespace=namespace)
                yield defer.succeed(queryResult)
                driver.next()
            except Exception, ex:
                log.debug("Exception collecting query: %s", str(ex))
                self.close()
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


def WmiGet(url, query, properties):
    from Products.DataCollector.DeviceProxy import DeviceProxy
    from WMIPlugin import WMIPlugin

    url  = url.split('/', 3)
    device = DeviceProxy()
    url[2], device.zWmiProxy = url[2].split('@')
    device.zWinUser, device.zWinPassword = url[2].split(':')
    device.id = device.zWmiProxy
    device.manageIp = device.zWmiProxy
    ns = url[3]

    if query.upper().startswith('SELECT '):
        cn = query
        kb = {}
    else:
        try:
            cn, keys = query.split('.', 1)
            kb = {}
            for key in keys.split(','):
                var, val = key.split('=')
                kb[var] = val
        except:
            cn = query
            kb = {}

    wp = WMIPlugin()
    wp.tables = {'t': (cn, kb, ns, properties)}
    cl = WMIClient(device=device, plugins=[wp,])
    cl.run()
    reactor.run()
    for plugin, result in cl.getResults():
        if plugin == wp:
            return result['t']
    return


if __name__ == "__main__":
    url = "//username:password@127.0.0.1/root/cimv2"
    query = 'CIM_Processor'
    properties = []
    aliases = []
    import getopt, sys
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
            url = arg
        elif opt in ("-q", "--query"):
            query = arg
        elif opt in ("-f", "--fields"):
            properties = arg.split()
        elif opt in ("-a", "--aliases"):
            aliases = arg.split()
    properties = dict(zip(properties, aliases))
    if len(properties) > 0:
        properties['__path'] = '__path'
    results = WmiGet(url, query, properties)
    if type(results) is not list:
        if results is not None: print results
        sys.exit(1)
    for res in results:
        if isinstance(res, CError):
            print res.getErrorMessage()
        else:
            print "InstanceName: %s"%res['__path']
            if len(results) == 1:
                for var, val in res.items():
                    if var == '__path': continue
                    if var in properties.values():
                        var = properties.keys()[properties.values().index(var)]
                    print "%s = %s"%(var, val)

