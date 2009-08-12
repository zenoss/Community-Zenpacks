################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OdbcDataSource

Defines attributes for how a datasource will be graphed
and builds the nessesary DEF and CDEF statements for it.

$Id: OdbcDataSource.py,v 1.0 2009/05/15 16:33:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel import RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions

from Products.ZenUtils.Utils import executeStreamCommand
import pyodbc

import cgi, time


class OdbcDataSource(RRDDataSource.RRDDataSource, ZenPackPersistence):

    ZENPACKID = 'ZenPacks.community.ZenODBC'

    sourcetypes = ('ODBC',)
    sourcetype = 'ODBC'
    cs = ''
    sql = ''

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id':'cs', 'type':'string', 'mode':'w'},
        {'id':'sql', 'type':'string', 'mode':'w'},
        )

    _relations = RRDDataSource.RRDDataSource._relations + (
        )
    
    # Screen action bindings (and tab definitions)
    factory_type_information = ( 
    { 
        'immediate_view' : 'editODBCDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit'
            , 'name'          : 'Data Source'
            , 'action'        : 'editODBCDataSource'
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

    def zmanage_editProperties(self, REQUEST=None):
        'add some validation'
        if REQUEST:
            self.cs = REQUEST.get('cs', '')
            self.sql = REQUEST.get('sql', '')
        return RRDDataSource.RRDDataSource.zmanage_editProperties(
                                                                self, REQUEST)

    def getQuery(self, context):
        cs = RRDDataSource.RRDDataSource.getCommand(self, context, self.cs)
        sql = RRDDataSource.RRDDataSource.getCommand(self, context, self.sql)
        fields = [dp.id for dp in self.getRRDDataPoints()]
        return (cs, sql, fields)


    security.declareProtected('Change Device', 'manage_testDataSource')
    def manage_testDataSource(self, testDevice, REQUEST):
        ''' Test the datasource by executing the command and outputting the
        non-quiet results.
        '''
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
        
        # Determine which device to execute against
        device = None
        if testDevice:
            # Try to get specified device
            device = self.findDevice(testDevice)
            if not device:
                REQUEST['message'] = 'Cannot find device matching %s' % testDevice
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
            REQUEST['message'] = 'Cannot determine a device to test against.'
            return self.callZenScreen(REQUEST)

        # Render
        header, footer = self.commandTestOutput().split('OUTPUT_TOKEN')
        out.write(str(header))
        cs, query, fields = self.getQuery(device)
        csa = dict([prop.split('=') for prop in cs.split(';')])
        if csa.has_key('PWD'):
            csa['PWD'] = '*****'
            csa = ';'.join([var + '=' + val for var, val in csa.iteritems()])
        else:
            csa = cs
        write('Executing query %s against %s' %(query, csa))
        write('')
        start = time.time()
        try:
            cnxn = pyodbc.connect(cs)
            cursor = cnxn.cursor()
            for q in query.split(';'):
                if not q.strip('\n '): continue
                cursor.execute(q.strip('\n '))
            output = cursor.fetchall()
            try:
                r = dict(output)
                values = {}
                for field in fields:
                    values[field] = r[field]
                write('%s' %values)
            except:
                for r in output:
                    write('%s' %dict(zip(fields, r)))
        except:
            import sys
            write('exception while executing query')
            write('type: %s  value: %s' % tuple(sys.exc_info()[:2]))
        write('')
        write('')
        write('DONE in %s seconds' % long(time.time() - start))
        out.write(str(footer))
