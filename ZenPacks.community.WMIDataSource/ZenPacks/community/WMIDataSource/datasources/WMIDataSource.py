################################################################################
#
# This program is part of the WMIDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WMIDataSource

Defines attributes for how a datasource will be graphed
and builds the nessesary DEF and CDEF statements for it.

$Id: WMIDataSource.py,v 1.1 2009/06/12 12:52:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel import RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions

from Products.ZenEvents.ZenEventClasses import Cmd_Fail
from Products.ZenUtils.Utils import executeStreamCommand
import cgi, time
import os

wmictemplate = ("wmic -U '${dev/zWinUser}'%%'%s' //%s --namespace='%s' \"%s\"")

class WMIDataSource(ZenPackPersistence, RRDDataSource.RRDDataSource):

    ZENPACKID = 'ZenPacks.community.WMIDataSource'

    sourcetypes = ('WMI',)
    sourcetype = 'WMI'
    namespace = 'root\cimv2'
    wql = ''

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id':'namespace', 'type':'string', 'mode':'w'},
        {'id':'wql', 'type':'string', 'mode':'w'},
        )

    _relations = RRDDataSource.RRDDataSource._relations + (
        )
    
    # Screen action bindings (and tab definitions)
    factory_type_information = ( 
    { 
        'immediate_view' : 'editWMIDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit'
            , 'name'          : 'Data Source'
            , 'action'        : 'editWMIDataSource'
            , 'permissions'   : ( Permissions.view, )
            },
        )
    },
    )

    security = ClassSecurityInfo()


    def getDescription(self):
        return self.wql

    def useZenCommand(self):
        return False

    def zmanage_editProperties(self, REQUEST=None):
        'add some validation'
        if REQUEST:
            self.namespace = REQUEST.get('namespace', '')
            self.wql = REQUEST.get('wql', '')
        return RRDDataSource.RRDDataSource.zmanage_editProperties(
                                                                self, REQUEST)

    def getCommand(self, context, password='${dev/zWinPassword}'):
        if self.namespace.startswith("\\\\"):
	    t1, t2, manageIp, namespace = self.namespace.split('\\', 3)
	else:
	    manageIp = "${dev/manageIp}"
	    namespace = self.namespace
        cmd = wmictemplate %(password, manageIp, namespace, self.wql)
        cmd = RRDDataSource.RRDDataSource.getCommand(self, context, cmd)
        return cmd

    def checkCommandPrefix(self, context, cmd):
        return cmd

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

        # Get the command to run
        command = self.getCommand(device)
	dCommand = self.getCommand(device, password='*****')
        # Render
        header, footer = self.commandTestOutput().split('OUTPUT_TOKEN')
        out.write(str(header))
        
        write('Executing command %s against %s' %(dCommand, device.id))
        write('')
        start = time.time()
        try:
            executeStreamCommand(command, write)
        except:
            import sys
            write('exception while executing command')
            write('type: %s  value: %s' % tuple(sys.exc_info()[:2]))
        write('')
        write('')
        write('DONE in %s seconds' % long(time.time() - start))
        out.write(str(footer))
