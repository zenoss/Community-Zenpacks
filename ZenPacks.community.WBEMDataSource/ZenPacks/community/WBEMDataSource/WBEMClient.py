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

$Id: WBEMClient.py,v 1.3 2009/12/20 20:26:23 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

import Globals
from Products.ZenUtils.Driver import drive
from Products.DataCollector.BaseClient import BaseClient
from ZenPacks.community.WBEMDataSource.lib import pywbem

from twisted.internet import defer, reactor
import socket

import time
import logging
log = logging.getLogger("zen.WBEMClient")


class BadCredentials(Exception): pass


class CError:

    errormsg = ''
    
    def __init__(self, errormsg):
        self.errormsg = errormsg
        
    def getErrorMessage(self):
        return self.errormsg


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


    def parseError(self, err, instMap):
        if type(instMap) is not dict:
            if str(err.type).split('.')[-1] == 'CIMError':
                return {instMap: [CError(err.value[1])]}
            return {instMap: [CError(err.value)]}
        result = {}
        for key, val in instMap.iteritems():
            if str(err.type).split('.')[-1] == 'CIMError':
                result[val[0]] = [CError(err.value[1])]
            else:
                result[val[0]] = [CError(err.value)]
        return result


    def parseValue(self, value):
	if isinstance(value, pywbem.Uint16): return int(value)
	if isinstance(value, pywbem.Uint32): return int(value)
	if isinstance(value, pywbem.Uint64): return int(value)
	if isinstance(value, pywbem.Sint16): return int(value)
	if isinstance(value, pywbem.Sint32): return int(value)
	if isinstance(value, pywbem.Sint64): return int(value)
	if isinstance(value, pywbem.Real32): return float(value)
	if isinstance(value, pywbem.Real64): return float(value)
	if isinstance(value, pywbem.CIMDateTime): return value.datetime
	return value


    def parseInstance(self, instance, properties={}):
        if len(properties) == 0:
	     properties = instance.properties.keys()
	if type(properties) is not dict:
	     properties = dict(zip(properties, properties))
        idict = {}
	for name, aname in properties.iteritems():
	    if name not in instance.properties: continue
	    prop = instance.properties[name]
	    if prop.is_array and prop.value:
	        idict[aname] = [self.parseValue(v) for v in prop.value]
	    else:
	        idict[aname] = self.parseValue(prop.value)
	    if 'Values' not in prop.qualifiers: continue
	    try:
	        idx = prop.qualifiers['ValueMap'].value.index(str(prop.value))
	        idict[aname] = prop.qualifiers['Values'].value[idx]
	    except: pass
	idict[properties.get('__path', '__path')] = instance.path
	return idict


    def _wbemEnumerateInstances(self, classname, namespace, instMap, qualifier):
        def parse(instances):
            result = {}
            for instance in instances:
	        for kbKey, kbVal in instMap.iteritems():
	            kb = []
	            if kbKey is None or kbKey is 'WQL':
		        table, props = kbVal
		    else:
		        try:
		            kbIns=tuple([instance[k] for k in kbKey])
		            if kbIns not in kbVal: continue
			except: continue
                        table, props = kbVal[kbIns]
                    if table not in result:
                        result[table] = []
                    result[table].append(self.parseInstance(instance, props))
            return result
            
        d = defer.maybeDeferred(self._wbem.EnumerateInstances,
                                                    classname,
                                                    namespace=namespace,
                                                    includeQualifiers=qualifier,
                                                    localOnly=False)
        d.addCallback(parse)
        d.addErrback(self.parseError, instMap)
        return d


    def _wbemExecQuery(self, query, namespace, instMap, qualifier):
        def parse(instances):
            tableName, props = instMap['WQL']
	    if isinstance(instances, pywbem.CIMInstance):
	        instances = [instances]
            return {tableName: [self.parseInstance(i, props) for i in instances]}
	    
        d = defer.maybeDeferred(self._wbem.ExecQuery,
                                            'WQL',
                                            query,
                                            namespace=namespace)
        d.addCallback(parse)
        d.addErrback(self.parseError, instMap['WQL'][0])
        return d


    def _wbemGetInstance(self, classname, namespace, instMap, qualifier):
        def parse(instance):
            tableName, props = instMap.values()[0].values()[0]
            return {tableName: [self.parseInstance(instance, props)]}
	    
        keybindings = dict(zip(instMap.keys()[0],
	                       instMap.values()[0].keys()[0]))
        instancename = pywbem.CIMInstanceName(classname, keybindings,
                                                    namespace=namespace)
        d = defer.maybeDeferred(self._wbem.GetInstance, instancename,
                                                    includeQualifiers=qualifier,
                                                    localOnly=False)
        d.addCallback(parse)
        d.addErrback(self.parseError, instMap.values()[0].values()[0][0])
        return d


    def query(self, queries, includeQualifiers=False):
        instMap = {}
        for tableName, query in queries.iteritems():
            classname, keybindings, namespace, properties = query
            classkey = (namespace, classname)
            if classkey not in instMap:
                instMap[classkey] = {}
            if type(keybindings) is dict:
                instkey = tuple(keybindings.keys())
		instval = tuple(keybindings.values())
		if instkey not in instMap[classkey]:
		    instMap[classkey][instkey] = {}
                instMap[classkey][instkey][instval]=(tableName, properties)
            else:
                instMap[classkey][keybindings]=(tableName, properties)
	return self.sortedQuery(instMap, includeQualifiers=includeQualifiers)


    def sortedQuery(self, queries, includeQualifiers=False):
        def inner(driver):
            try:
                queryResult = {}
                for (namespace, classname), instMap in queries.iteritems():
                    if 'WQL' in instMap:
                        yield self._wbemExecQuery(classname, namespace,
                                                    instMap, includeQualifiers)
                    elif None in instMap:
                        yield self._wbemEnumerateInstances(classname, namespace,
                                                    instMap, includeQualifiers)
                    elif len(instMap) and len(instMap.values()[0]) == 1:
                        yield self._wbemGetInstance(classname, namespace,
                                                    instMap, includeQualifiers)
                    else:
                        yield self._wbemEnumerateInstances(classname, namespace,
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
                    log.debug("Queries: %s" % str(plugin.queries()))
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

def WbemGet(url, query, properties):
    from Products.DataCollector.DeviceProxy import DeviceProxy
    from WBEMPlugin import WBEMPlugin

    url  = url.split('/', 3)
    device = DeviceProxy()
    device.zWbemUseSSL = True and url[0].lower() == 'https:' or False
    device.zWinUser, url[2], device.zWbemPort = url[2].split(':')
    device.zWinPassword, device.zWbemProxy = url[2].split('@')
    device.id = device.zWbemProxy
    device.manageIp = device.zWbemProxy
    ns = url[3]

    if query.upper().startswith('SELECT '):
        cn = query
        kb = 'WQL'
    else:
        try:
            cn, keys = query.split('.', 1)
            kb = {}
            for key in keys.split(','):
                var, val = key.split('=')
                kb[var] = val.strip('"')
        except:
            cn = query
            kb = None

    wp = WBEMPlugin()
    wp.tables = {'t': (cn, kb, ns, properties)}
    cl = WBEMClient(device=device, plugins=[wp,])
    cl.run()
    reactor.run()
    for plugin, result in cl.getResults():
        if plugin == wp:
            return result['t']
    return


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
        if isinstance(res, CError):
            print res.getErrorMessage()
        else:
            print "InstanceName: %s"%res['__path']
            if len(results) == 1:
                for var, val in res.items():
                    if var == '__path': continue
                    print "%s = %s"%(var, val)

