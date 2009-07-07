################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OdbcPlugin

wrapper for PythonPlugin

$Id: OdbcPlugin.py,v 1.0 2009/05/15 16:29:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

from twisted.internet import defer, reactor, protocol

from ZenPacks.community.ZenODBC.parsers.isql import parseResults, connectionString 


class isqlPP(protocol.ProcessProtocol):

    def __init__(self, deferred, tables):
        self.deferred = deferred
        self.res = {}
        self.tmap = []
        self.sql = []
        for tnames, tq in tables.iteritems():
            self.tmap.append((tnames, tq[1]))
            self.sql.append(tq[0])
	self.data = {}

    def connectionMade(self):
        for sql in self.sql:
            self.transport.write(sql + '\n')
	    self.transport.closeStdin()

    def outReceived(self, text):
        lines = ''
        counter = 0
        for line in text.split('\n'):
            if not line.startswith('SQL>'):
                lines = lines + line + '\n'
            else:
                counter = counter + 1
                if counter > 1:
                    table,columns = self.tmap[counter - 2]
		    if not lines.startswith('['):
                        self.data[table] = parseResults(lines, columns)
		    else: self.data[table] = ''
                lines = line[5:] + '\n'
                

    def getdata(self):
        return self.data

    def processEnded(self, reason):
        if self.deferred is not None:
            self.deferred.callback(self.getdata())


class OdbcPlugin(PythonPlugin):
    

    ZENPACKID = 'ZenPacks.community.ZenODBC'

    transport = "python"
    maptype = "OdbcPlugin"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.RDBMS.Database"

    cs = ""
    tables = {'default': ('sql', []),}
    uid = None
    pwd = None

    def prepare(self, device, log):
	return (self.cs, self.tables, self.uid, self.pwd)
	
    def collect(self, device, log):
	(cs, tables, uid, pwd) = self.prepare(device, log)
	cs = connectionString(cs, uid=uid, pwd=pwd)
        args = ("isql", "-v", "-d|") + tuple(cs.isqlArgs())
        d = defer.Deferred()
        reactor.spawnProcess(isqlPP(d, tables), 'isql', args, {}, '.')
        return d
    
    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        return rm

