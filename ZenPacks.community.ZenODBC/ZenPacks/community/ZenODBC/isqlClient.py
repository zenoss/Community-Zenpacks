################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""isqlClient

Gets ODBC performance data with isql command.

$Id: isqlClient.py,v 1.0 2009/12/01 23:38:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from twisted.internet import defer, reactor, protocol
from ZenPacks.community.ZenODBC.OdbcClient import CError

import ConfigParser
import os


class isqlPP(protocol.ProcessProtocol):

    def __init__(self, deferred, tables):
        self.deferred = deferred
        self.res = {}
        self.tmap = [(None, None)]
        self.sql = []
        for table, queries, fields in tables:
            for query in queries.split(';'):
                if query.strip(' \n'):
                    self.sql.append(query.strip(' \n'))
                    self.tmap.append((None, None))
            self.tmap.pop()
            self.tmap.append((table, fields))
	self.data = {}
	self.text = ''


    def connectionMade(self):
        for sql in self.sql:
            self.transport.write(sql + ';\n')
	self.transport.closeStdin()


    def outReceived(self, text):
        self.text = self.text + text
    
    def outConnectionLost(self):
        lines = ''
        for line in self.text.split('\n'):
            if not line.startswith('SQL>'):
                lines = lines + line + '\n'
            else:
                table,columns = self.tmap.pop(0)
                if table:
		    if not lines.startswith('['):
                        self.data[table] = self.parseResults(lines, columns)
		    else:
		        self.data[table] = [CError(lines)]
                lines = line[5:] + '\n'
                if lines.startswith('SQL>'):
                    lines = lines[5:]
                    self.tmap.pop(0)
            
    def getdata(self):
        return self.data

    def parseResults(self, output, header):
        lines = output.strip().split('\n')
        if len(lines[0].split('|')) == 2:
	    prop = []
	    theader = []
	    for line in lines:
	        try:
	            line = line.split('|')
	        except: continue
	        if line[0] in header:
		    theader.append(line[0])
		    prop.append(line[1])
	    if not (set(header) ^ set(theader)):
	        lines = ['|'.join(prop),]
	        header = theader
        results = []
        for line in lines:
            prop = {}
            try:
	        line = line.split('|')
	    except: continue
	    for dp,value in zip(header, line):
	        if not value: value = ''
	        if str(value).isdigit(): value = int(value)
                prop[dp] = value
            results.append(prop)
        return results


    def processEnded(self, reason):
        if self.deferred is not None:
            self.deferred.callback(self.getdata())

class connectionString:
    
    def __init__(self, cs, uid=None, pwd=None, context=None):
        self.uid = uid
        self.pwd = pwd
        if context is not None:
	    self.cs = talesEval('string:' + cs, context)
	else: self.cs = cs
	self.parseConnectionString()

    def parseConnectionString(self):
	self.config = ConfigParser.RawConfigParser()
	self.config.add_section('ODBC')
	for item in self.cs.split(';'):
	    var,val = item.split('=')
	    self.config.set('ODBC', var.strip(), val.strip('{} '))
	if self.config.has_option('ODBC', 'UID'):
	    if self.uid is None: self.uid = self.config.get('ODBC', 'UID')
	    self.config.remove_option('ODBC', 'UID')
	if self.config.has_option('ODBC', 'PWD'):
	    if self.pwd is None: self.pwd = self.config.get('ODBC', 'PWD')
	    self.config.remove_option('ODBC', 'PWD')
        if self.config.has_option('ODBC', 'FILEDSN'):
	    self.readDsnFromFile()
	    self.config.remove_option('ODBC', 'FILEDSN')
        if self.config.has_option('ODBC', 'DSN'):
	    self.dsn = self.config.get('ODBC', 'DSN')
	    self.config.remove_option('ODBC', 'DSN')
	else: self.updateOdbcIni()

    def readDsnFromFile(self, dsnfile):
        self.config.remove_section('ODBC')
	self.config.read(dsnfile)
	sourcedsn = self.config.sections()[0]
	if self.uid is None: self.uid = self.config.get(sourcedsn, 'UID')
	if self.pwd is None: self.pwd = self.config.get(sourcedsn, 'PWD')
	self.config.remove_option(sourcedsn, 'UID')
	self.config.remove_option(sourcedsn, 'PWD')

    def updateOdbcIni(self):    
        import md5
	self.dsn = md5.new(self.cs).hexdigest()
        odbcinifile = os.path.expanduser('~/.odbc.ini')
	odbcini = ConfigParser.RawConfigParser()
	try:
	    fp = open(odbcinifile)
	    odbcini.readfp(fp)
	    fp.close()
	except: pass
	if not odbcini.has_section(self.dsn):
	    odbcini.add_section(self.dsn)
	    for item in self.config.items(self.config.sections()[0]):
		odbcini.set(self.dsn, item[0], item[1])
	    fp = open(odbcinifile , 'wb')
	    odbcini.write(fp)
	    fp.close()

    def isqlArgs(self):
        ret = [self.dsn,]
        if self.uid is not None:
            ret.append(self.uid)
            if self.pwd is not None: ret.append(self.pwd)
        return ret



class isqlClient:

    def __init__(self, cs):
        self.results = {}
	cs = connectionString(cs)
        self.isqlArgs = ("isql", "-v", "-d|") + tuple(cs.isqlArgs())


    def query(self, tables):
        d = defer.Deferred()
        reactor.spawnProcess(isqlPP(d, tables), 'isql', self.isqlArgs, {}, '.')
        return d
