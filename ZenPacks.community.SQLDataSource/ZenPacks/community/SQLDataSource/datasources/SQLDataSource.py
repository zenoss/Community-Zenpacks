################################################################################
#
# This program is part of the SQLDataSource Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SQLDataSource

Defines attributes for how a datasource will be graphed
and builds the nessesary DEF and CDEF statements for it.

$Id: SQLDataSource.py,v 1.1 2010/08/24 20:10:52 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel import RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenUtils.Utils import executeStreamCommand
from Products.ZenWidgets import messaging
from AccessControl import ClassSecurityInfo, Permissions

import cgi, time
import os

class SQLDataSource(ZenPackPersistence, RRDDataSource.RRDDataSource):

    ZENPACKID = 'ZenPacks.community.SQLDataSource'

    sourcetypes = ('SQL',)
    sourcetype = 'SQL'
    cs = ''
    sql = ''
    sqlparsed = ''
    sqlkb = {}

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id':'cs', 'type':'string', 'mode':'w'},
        {'id':'sql', 'type':'string', 'mode':'w'},
        )

    _relations = RRDDataSource.RRDDataSource._relations + (
        )

    # Screen action bindings (and tab definitions)
    factory_type_information = ( 
    { 
        'immediate_view' : 'editSQLDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit'
            , 'name'          : 'Data Source'
            , 'action'        : 'editSQLDataSource'
            , 'permissions'   : ( Permissions.view, )
            },
        )
    },
    )

    security = ClassSecurityInfo()


    def getDescription(self):
        return self.sql

    def useZenCommand(self):
        return False


    def checkCommandPrefix(self, context, cmd):
        """
        Overriding method to verify that zCommandPath is not prepending to our
        Instance name or Query statement.
        """
        return cmd


    def zmanage_editProperties(self, REQUEST=None):
        'add some validation'
        if REQUEST:
            self.cs = REQUEST.get('cs', '')
            self.sql = REQUEST.get('sql', '')
            self.sqlparsed, self.sqlkb = self.parseSqlQuery(self.sql)
        return RRDDataSource.RRDDataSource.zmanage_editProperties(self, REQUEST)


    def parseSqlQuery(self, sql):
        keybindings = {}
        if sql == '': return '', {}
        try:
            newsql, where = sql.rsplit(' WHERE ', 1)
            wheres = ['',]
            for token in where.split():
                if token.upper() in ('LIMIT', 'OR', 'NOT'): raise
                if token.upper() in ('GO', ';'): continue
                if token.upper() == 'AND': wheres.append('')
                wheres[-1] = wheres[-1] + ' ' + token
            newwhere = []
            for kb in wheres:
                var, val = kb.split('=')
                if newsql.find('%s'%var.strip()) == -1: newwhere.append(kb)
                else: keybindings[var.strip()] = val.strip()
            if keybindings:
                sql = newsql
                if newwhere: sql = sql + ' WHERE %s AND '%' AND '.join(newwhere)
        except: return sql, {}
        return sql, keybindings


    def getConnectionString(self, context):
        return RRDDataSource.RRDDataSource.getCommand(self, context, self.cs)


    def getQueryInfo(self, context):
        if self.sqlparsed == '':
            self.sqlparsed, self.sqlkb = self.parseSqlQuery(self.sql)
        sql=RRDDataSource.RRDDataSource.getCommand(self,context,self.sqlparsed)
        if self.sqlkb == {}: keybindings = {}
        else:
            keybindings = dict(zip(self.sqlkb.keys(),
                                RRDDataSource.RRDDataSource.getCommand(self,
                                context,
                                ', '.join(self.sqlkb.values())).split(', ')))
        return (sql, keybindings, self.getConnectionString(context))


    def testDataSourceAgainstDevice(self, testDevice, REQUEST, write, errorLog):
        """
        Does the majority of the logic for testing a datasource against the device
        @param string testDevice The id of the device we are testing
        @param Dict REQUEST the browers request
        @param Function write The output method we are using to stream the result of the command
        @parma Function errorLog The output method we are using to report errors
        """ 
        out = REQUEST.RESPONSE
        # Determine which device to execute against
        device = None
        if testDevice:
            # Try to get specified device
            device = self.findDevice(testDevice)
            if not device:
                errorLog(
                    'No device found',
                    'Cannot find device matching %s.' % testDevice,
                    priority=messaging.WARNING
                )
                return self.callZenScreen(REQUEST)
        elif hasattr(self, 'device'):
            # ds defined on a device, use that device
            device = self.device()
        elif hasattr(self, 'getSubDevicesGen'):
            # ds defined on a device class, use any device from the class
            try:
                device = self.getSubDevicesGen().next()
            except StopIteration:
                # No devices in this class, bail out
                pass
        if not device:
            errorLog(
                'No Testable Device',
                'Cannot determine a device against which to test.',
                priority=messaging.WARNING
            )
            return self.callZenScreen(REQUEST)

        header = ''
        footer = ''
        # Render
        if REQUEST.get('renderTemplate', True):
            header, footer = self.commandTestOutput().split('OUTPUT_TOKEN')

        out.write(str(header))

        try:
            import sys
            cs = self.getConnectionString(device)
            sql = RRDDataSource.RRDDataSource.getCommand(self, device, self.sql)
            properties = dict([(
                        dp.getAliasNames() and dp.getAliasNames()[0] or dp.id,
                        dp.id) for dp in self.getRRDDataPoints()])
            write('Executing query: "%s"'%sql)
            write('')
            zp = self.dmd.ZenPackManager.packs._getOb(
                                    'ZenPacks.community.SQLDataSource', None)
            command = "env PYTHONPATH=\"%s\" python %s -c \"%s\" -q \"%s\" -f \"%s\" -a \"%s\""%(
                                                os.pathsep.join(sys.path),
                                                zp.path('SQLClient.py'),cs,sql,
                                                " ".join(properties.keys()),
                                                " ".join(properties.values()))
            start = time.time()
            executeStreamCommand(command, write)
        except:
            import sys
            write('exception while executing command')
            write('type: %s  value: %s' % tuple(sys.exc_info()[:2]))
        write('')
        write('')
        write('DONE in %s seconds' % long(time.time() - start))
        out.write(str(footer))


    security.declareProtected('Change Device', 'manage_testDataSource')
    def manage_testDataSource(self, testDevice, REQUEST):
        ''' Test the datasource by executing the command and outputting the
        non-quiet results.
        '''
        # set up the output method for our test
        out = REQUEST.RESPONSE
        def write(lines):
            ''' Output (maybe partial) result text.
            '''
            # Looks like firefox renders progressive output more smoothly
            # if each line is stuck into a table row.  
            startLine = '<tr><td class="tablevalues">'
            endLine = '</td></tr>\n'
            if out:
                if not isinstance(lines, list):
                    lines = [lines]
                for l in lines:
                    if not isinstance(l, str):
                        l = str(l)
                    l = l.strip()
                    l = cgi.escape(l)
                    l = l.replace('\n', endLine + startLine)
                    out.write(startLine + l + endLine)

        # use our input and output to call the testDataSource Method
        errorLog = messaging.IMessageSender(self).sendToBrowser
        return self.testDataSourceAgainstDevice(testDevice,
                                                REQUEST,
                                                write,
                                                errorLog)
