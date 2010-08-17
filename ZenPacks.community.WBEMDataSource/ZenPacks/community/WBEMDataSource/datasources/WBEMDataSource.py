################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WBEMDataSource

Defines attributes for how a datasource will be graphed
and builds the nessesary DEF and CDEF statements for it.

$Id: WBEMDataSource.py,v 1.9 2010/08/17 22:42:14 egor Exp $"""

__version__ = "$Revision: 1.9 $"[11:-2]

from Products.ZenModel import RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenUtils.Utils import executeStreamCommand
from Products.ZenWidgets import messaging
from AccessControl import ClassSecurityInfo, Permissions

import cgi, time
import os

class WBEMDataSource(ZenPackPersistence, RRDDataSource.RRDDataSource):

    ZENPACKID = 'ZenPacks.community.WBEMDataSource'

    sourcetypes = ('WBEM',)
    sourcetype = 'WBEM'
    namespace = 'root/cimv2'
    instance = ''

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id':'namespace', 'type':'string', 'mode':'w'},
        {'id':'instance', 'type':'string', 'mode':'w'},
        )

    _relations = RRDDataSource.RRDDataSource._relations + (
        )

    # Screen action bindings (and tab definitions)
    factory_type_information = ( 
    { 
        'immediate_view' : 'editWBEMDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit'
            , 'name'          : 'Data Source'
            , 'action'        : 'editWBEMDataSource'
            , 'permissions'   : ( Permissions.view, )
            },
        )
    },
    )

    security = ClassSecurityInfo()


    def getDescription(self):
        return self.instance

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
            self.namespace = REQUEST.get('namespace', '')
            self.instance = REQUEST.get('instance', '')
        return RRDDataSource.RRDDataSource.zmanage_editProperties(
                                                                self, REQUEST)

    def getInstanceInfo(self, context):
        classname = RRDDataSource.RRDDataSource.getCommand(self, context,
                                                            self.instance)
        namespace = RRDDataSource.RRDDataSource.getCommand(self, context,
                                                            self.namespace)
        transport = self.sourcetype
        if classname.upper().startswith('SELECT '):
            return (transport, classname, {}, namespace)
        kb = classname.split('.', 1)
        cn = kb[0].split(':', 1)
        if len(cn) > 1:
            classname = cn[1]
            namespace = cn[0]
        else: classname = cn[0]
        if len(kb) > 1: kb = kb[1]
        else: return (transport, classname, {}, namespace)
        keybindings = {}
        for key in kb.split(','):
            try: var, val = key.split('=', 1)
            except: continue
            keybindings[var] = val
        return (transport, classname, keybindings, namespace)


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
            tr, inst, kb, namespace = self.getInstanceInfo(device)
            inst = RRDDataSource.RRDDataSource.getCommand(self, device,
                                                            self.instance)
            if inst.startswith("%s:"%namespace): inst = inst[len(namespace)+1:]
            properties = dict([(
                        dp.getAliasNames() and dp.getAliasNames()[0] or dp.id,
                        dp.id) for dp in self.getRRDDataPoints()])
            url='%s://%%s%s:%s/%s'%(device.zWbemUseSSL and 'https' or 'http',
                                    device.zWbemProxy or device.manageIp,
                                    device.zWbemPort, namespace)
            write('Get %s Instance %s from %s' % (tr, inst, str(url%'')))
            write('')
            creds = '%s:%s@'%(device.zWinUser, device.zWinPassword)
            zp = self.dmd.ZenPackManager.packs._getOb(
                                   'ZenPacks.community.%sDataSource'%tr, None)
            command = "python %s -c \"%s\" -q \'%s\' -f \"%s\" -a \"%s\""%(
                                                zp.path('%sClient.py'%tr),
                                                str(url%creds),
                                                inst.replace("'", '"'),
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
