################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""isql

isql connectionStrng ang CommandParser Objects

$Id: isql.py,v 1.0 2009/05/31 14:28:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenRRD.CommandParser import CommandParser
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenUtils.ZenTales import talesEval

import os, ConfigParser, md5

def parseResults(output, header):
    lines = output.strip().split('\n')
    if len(lines[0].split('|')) == 2:
	prop = []
	theader = []
	for line in lines:
	    line = line.split('|')
	    if line[0] in header:
		theader.append(line[0])
		prop.append(line[1])
	if not (set(header) ^ set(theader)):
	    lines = ['|'.join(prop),]
	    header = theader
    results = []
    for line in lines:
        prop = {}
	line = line.split('|')
	for dp,value in zip(header, line):
	    if not value: value = ''
	    if str(value).isdigit(): value = int(value)
            prop[dp] = value
        results.append(prop)
    return results


class isql(CommandParser):

    def processResults(self, cmd, result):
        values = ''
        if cmd.result.exitCode == 0:
            results = parseResults( cmd.result.output,
                                    [ds.id for ds in cmd.points])
            severity = 0
            msg = 'OK'
            for dp in cmd.points:
                value = results[0].get(dp.id, None)
                result.values.append( (dp, value) )
                values = values + str(dp.id) + '=' + str(value) + ' ' 
        else:
            severity = cmd.severity
            msg = cmd.result.output
        result.events.append(dict(device = cmd.deviceConfig.device,
                                  summary = msg,
                                  severity = severity,
                                  message = msg,
                                  performanceData = values,
                                  eventKey = cmd.eventKey,
                                  eventClass = cmd.eventClass,
                                  component = cmd.component))
        return result


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
	    if self.uid is None: self.uid = config.get('ODBC', 'UID')
	    self.config.remove_option('ODBC', 'UID')
	if self.config.has_option('ODBC', 'PWD'):
	    if self.pwd is None: self.pwd = config.get('ODBC', 'PWD')
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
        if self.uid is not None: ret.append(self.uid)
        if self.pwd is not None: ret.append(self.pwd)
        return ret
