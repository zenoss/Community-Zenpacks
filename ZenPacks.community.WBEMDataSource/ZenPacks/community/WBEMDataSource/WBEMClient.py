################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WBEMClient

Gets WBEM performance data.

$Id: WBEMClient.py,v 2.9 2010/07/01 13:58:53 egor Exp $"""

__version__ = "$Revision: 2.9 $"[11:-2]

import Globals
from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.Driver import drive
from Products.DataCollector.BaseClient import BaseClient
from ZenPacks.community.WBEMDataSource.lib import pywbem
from ZenPacks.community.WBEMDataSource.services.WbemPerfConfig import sortQuery

from twisted.internet import defer, reactor
from twisted.python.failure import Failure
from DateTime import DateTime

import os
import socket
import sys
import logging
log = logging.getLogger("zen.WBEMClient")

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


class BadCredentials(Exception): pass


class WBEMClient(BaseClient):

    def __init__(self, device, datacollector=None, plugins=[]):
        BaseClient.__init__(self, device, datacollector)
        self.device = device
        self.host = device.id
        if device.zWbemProxy is not "":
            self.host = device.zWbemProxy
        elif socket.getfqdn().lower() == device.id.lower(): 
            self.host = "."
        elif device.manageIp is not None:
            self.host = device.manageIp
        self.name = device.id
        self.url = '%s://%s:%s' % (
                        device.zWbemUseSSL and 'https' or 'http',
                        self.host,
                        device.zWbemPort)
        self.creds = (device.zWinUser, device.zWinPassword)
        self._wbem = pywbem.WBEMConnection(self.url, self.creds, 
                                            default_namespace='root/cimv2')
        self.datacollector = datacollector
        self.plugins = plugins
        self.results = []


    def parseError(self, err, query, instMap):
        if isinstance(err.value, pywbem.cim_http.AuthError):
            msg = 'AuthError: Please check zWinUser and zWinPassword zProperties'
        else:
            msg = 'Received %s from query: %s'%(err.value[1], query)
        err = Failure(err)
        err.value = msg
        log.error(err.getErrorMessage())
        results = {}
        for instances in instMap.values():
            for tables in instances.values():
                for table, props in tables:
                    results[table] = [err]
        return results


    def parseValue(self, value):
        if isinstance(value, pywbem.Uint8): return int(value)
        if isinstance(value, pywbem.Uint16): return int(value)
        if isinstance(value, pywbem.Uint32): return int(value)
        if isinstance(value, pywbem.Uint64): return int(value)
        if isinstance(value, pywbem.Sint8): return int(value)
        if isinstance(value, pywbem.Sint16): return int(value)
        if isinstance(value, pywbem.Sint32): return int(value)
        if isinstance(value, pywbem.Sint64): return int(value)
        if isinstance(value, pywbem.Real32): return float(value)
        if isinstance(value, pywbem.Real64): return float(value)
        if isinstance(value, pywbem.CIMDateTime):
            try: return DateTime(value.datetime)
            except:
                t = value.datetime.utctimetuple()
                return DateTime(t[0],t[1],t[2],t[3],t[4],t[5],'GMT')
        return value


    def parseInstance(self, instance, properties={}):
        if len(properties) == 0:
             properties = instance.properties.keys()
        if type(properties) is not dict:
             properties = dict(zip(properties, properties))
        idict = {}
        for name, anames in properties.iteritems():
            if name not in instance.properties: continue
            prop = instance.properties[name]
            if 'Values' not in prop.qualifiers:
                if prop.is_array and prop.value:
                    idictp = [self.parseValue(v) for v in prop.value]
                else:
                    idictp = self.parseValue(prop.value)
            else:
                values = prop.qualifiers['Values'].value
                if 'ValueMap' in prop.qualifiers:
                    vmap = prop.qualifiers['ValueMap'].value
                else:
                    vmap = [str(i) for i in range(len(values))]
                if prop.is_array and prop.value:
                    idictp = []
                    for v in prop.value:
                        idx = vmap.index(str(v))
                        idictp.append(values[idx])
                else:
                    idx = vmap.index(str(prop.value))
                    idictp = values[idx]
            if type(anames) is not tuple: anames = (anames,)
            for aname in anames: idict[aname] = idictp
        idict[properties.get('__path', '__path')] = str(instance.path)
        return idict


    def _wbemEnumerateInstances(self, classname, namespace, instMap, qualifier):
        def parse(instances):
            results = {}
            for insts in instMap.values():
                for tables in insts.values():
                    for table, props in tables:
                        results[table] = []
            for instance in instances:
                for kbKey, kbVal in instMap.iteritems():
                    kbIns = []
                    if kbKey != ():
                        for k in kbKey:
                            val = instance[k.lower()]
                            if type(val) in [str, unicode]:
                                kbIns.append('"%s"'%val)
                            else:
                                kbIns.append(str(val))
                        if tuple(kbIns) not in kbVal: continue
                    for table, props in kbVal[tuple(kbIns)]:
                        results[table].append(self.parseInstance(instance,props))
            return results

        plst = set()
        for keyprops, insts in instMap.iteritems():
            for tables in insts.values():
                for (table, props) in tables:
                    if props == {}:
                        plst = []
                        break
                    plst = plst.union(props.keys())
                if plst == []: break
            if plst == []: break
            plst = plst.union(keyprops)
        try: plst.remove('__path')
        except: pass
        kwargs={"namespace":namespace,
                "IncludeQualifiers":qualifier,
                "LocalOnly":False}
        if plst: kwargs["PropertyList"] = list(plst)
        d=defer.maybeDeferred(self._wbem.EnumerateInstances,classname, **kwargs)
        d.addCallback(parse)
        d.addErrback(self.parseError, classname, instMap)
        return d


    def _wbemExecQuery(self, query, namespace, instMap, qualifier):
        def parse(instances):
            results = {}
            if isinstance(instances, pywbem.CIMInstance):
                instances = [instances]
            for table, props in instMap[()]:
                results[table]=[self.parseInstance(i,props) for i in instances]
            return results

        d = defer.maybeDeferred(self._wbem.ExecQuery,
                                            'WQL',
                                            query,
                                            namespace=namespace)
        d.addCallback(parse)
        d.addErrback(self.parseError, classname, instMap)
        return d


    def _wbemGetInstance(self, classname, namespace, instMap, qualifier):
        def parse(instance):
            results = {}
            for table, props in instMap.values()[0].values()[0]:
                results[table] = [self.parseInstance(instance, props)]
            return results

        keybindings = dict([(var, val.strip('"')) for var, val in zip(
                            instMap.keys()[0], instMap.values()[0].keys()[0])])
        plst = instMap.values()[0].values()[0][0][1].keys()
        try: plst.remove('__path')
        except: pass
        kwargs = {"IncludeQualifiers":qualifier, "LocalOnly":False}
        if plst: kwargs["PropertyList"] = list(plst)
        instancename = pywbem.CIMInstanceName(classname, keybindings,
                                                    namespace=namespace)
        d = defer.maybeDeferred(self._wbem.GetInstance, instancename, **kwargs)
        d.addCallback(parse)
        d.addErrback(self.parseError, classname, instMap)
        return d


    def query(self, queries, includeQualifiers=False):
        instMap = {}
        for table, query in queries.iteritems():
            instMap = sortQuery(instMap, table, query)
        return self.sortedQuery(instMap, includeQualifiers=includeQualifiers)


    def sortedQuery(self, queries, includeQualifiers=False):
        def inner(driver):
            try:
                queryResult = {}
                for namespace, classes in queries.iteritems():
                    for classname, instMap in classes.iteritems():
                        if classname.upper().startswith('SELECT '):
                            yield self._wbemExecQuery(classname, namespace,
                                                    instMap, includeQualifiers)
                        elif () in instMap or len(instMap) > 1 or \
                                                len(instMap.values()[0]) > 1:
                            yield self._wbemEnumerateInstances(classname,
                                        namespace, instMap, includeQualifiers)
                        else:
                            yield self._wbemGetInstance(classname, namespace,
                                                    instMap, includeQualifiers)
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
                        yield self.query(plugin.queries(self.device),
                                                    plugin.includeQualifiers)
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

def WbemGet(url, query, properties):
    from Products.DataCollector.DeviceProxy import DeviceProxy
    from WBEMPlugin import WBEMPlugin

    url  = url.rsplit('@', 1)
    device = DeviceProxy()
    device.zWbemProxy, ns = url[1].split('/', 1)
    device.zWbemProxy, device.zWbemPort = device.zWbemProxy.split(':')
    device.id = device.zWbemProxy
    device.manageIp = device.zWbemProxy
    url  = url[0].split('//', 1)
    device.zWinUser, device.zWinPassword = url[1].split(':', 1)
    device.zWbemUseSSL = True and url[0] == 'https:' or False

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

    wp = WBEMPlugin()
    wp.tables = {'t': (cn, kb, ns, properties)}
    wp.includeQualifiers = True
    cl = WBEMClient(device=device, plugins=[wp,])
    cl.run()
    reactor.run()
    for plugin, result in cl.getResults():
        if plugin == wp and 't' in result:
            return result['t']
    return result


if __name__ == "__main__":
    url = "https://username:password@127.0.0.1:5989/root/cimv2"
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
    results = WbemGet(url, query, properties)
    if type(results) is not list:
        print results
        sys.exit(1)
    for res in results:
        if isinstance(res, Failure):
            print res.getErrorMessage()
        else:
            print "InstanceName: %s"%res['__path']
            if len(results) == 1:
                for var, val in res.items():
                    if var == '__path': continue
                    if var in properties.values():
                        var = properties.keys()[properties.values().index(var)]
                    print "%s = %s"%(var, val)
