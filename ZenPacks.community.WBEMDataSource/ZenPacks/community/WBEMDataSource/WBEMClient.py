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

$Id: WBEMClient.py,v 1.1 2009/11/12 07:42:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenUtils.Driver import drive
from Products.DataCollector.BaseClient import BaseClient
from ZenPacks.community.WBEMDataSource.lib import pywbem

from twisted.internet import defer
import socket

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
                        device.zWbemProxy and device.zWbemProxy or self.host,
			device.zWbemPort)
        self.creds = (device.zWinUser, device.zWinPassword)
        self._wbem = pywbem.WBEMConnection(self.url, self.creds, 
                                            default_namespace='root/cimv2')
        self.datacollector = datacollector
        self.plugins = plugins
        self.results = []


    def _wbemEnumerateInstances(self, classname, namespace, instMap):
        def parse(instances):
	    result = {}
	    keybindings = ()
	    for instance in instances:
	        if () not in instMap:
		    cname, kb = str(instance.path).split('.', 1)
		    keybindings = tuple(sorted([i.split('=')[1].strip('"') for i in kb.split(',')]))
		if keybindings in instMap:
		    instance.PropertyList =instMap[keybindings][1]
		    if instMap[keybindings][0] not in result:
		        result[instMap[keybindings][0]] = []
		    result[instMap[keybindings][0]].append(instance)
	    return result

        d = defer.maybeDeferred(self._wbem.EnumerateInstances,
                                                    classname,
                                                    namespace=namespace,
                                                    includeQualifiers=True,
                                                    localOnly=False)
        d.addCallback(parse)
        return d

    def _wbemExecQuery(self, query, namespace, queryLang, tableName, properties):
        def parse(instances):
	    for instance in instances:
	        instance.PropertyList = properties
	    return {tableName: instances}

        d = defer.maybeDeferred(self._wbem.ExecQuery,
	                                    queryLang,
                                            query,
                                            namespace=namespace)
        d.addCallback(parse)
        return d

    def _wbemGetInstance(self, classname, namespace, keybindings, tableName,
                                                                properties):
        def parse(instance):
	    return {tableName: [instance]}
	
        instancename = pywbem.CIMInstanceName(classname, keybindings,
	                                            namespace=namespace)
        d = defer.maybeDeferred(self._wbem.GetInstance,
                                                    instancename,
						    PropertyList=properties,
                                                    includeQualifiers=True,
                                                    localOnly=False)
        d.addCallback(parse)
        return d


    def query(self, queries):
        def inner(driver):
            try:
                queryResult = {}
		instancesMap = {}
                for tableName, query in queries.iteritems():
		    classname, keybindings, namespace, properties = query
		    classkey = (namespace, classname)
		    if type(keybindings) is dict:
		        instkey = tuple(sorted(keybindings.values()))
		    else:
		        instkey = keybindings
		    if classkey not in instancesMap:
		        instancesMap[classkey] = {}
		    instancesMap[classkey][instkey] = (tableName, properties,
		                                                keybindings)
		for (namespace, classname), value in instancesMap.iteritems():
		    if len(instancesMap[(namespace, classname)]) == 1:
		        key,(tableName,properties,keybindings) = value.popitem()
		        if type(keybindings) is dict:
			    yield self._wbemGetInstance(classname, namespace,
			                    keybindings, tableName, properties)
			else:
			    yield self._wbemExecQuery(classname, namespace,
			                    keybindings, tableName, properties)
		    else:
                        yield self._wbemEnumerateInstances(classname, namespace,
		                            instancesMap[(namespace,classname)])
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
