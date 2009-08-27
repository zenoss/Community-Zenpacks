################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WBEMDataSource

Defines attributes for how a datasource will be graphed
and builds the nessesary DEF and CDEF statements for it.

$Id: WBEMDataSource.py,v 1.1 2009/06/12 12:52:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel import RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions

from ZenPacks.community.WBEMDataSource.lib import pywbem

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

    def zmanage_editProperties(self, REQUEST=None):
        'add some validation'
        if REQUEST:
            self.namespace = REQUEST.get('namespace', '')
            self.instance = REQUEST.get('instance', '')
        return RRDDataSource.RRDDataSource.zmanage_editProperties(
                                                                self, REQUEST)

    def getInstanceName(self, context):
        inst = RRDDataSource.RRDDataSource.getCommand(self, context, self.instance)
        try:
            classname, keys = inst.split('.', 1)
        except:
            return (inst, None, self.namespace)
        keybindings = {}
        for key in keys.split(','):
            var, val = key.split('=')
            keybindings[var] = val.strip('"')
        return (classname, keybindings, self.namespace)


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

        queries = {'test':
            RRDDataSource.RRDDataSource.getCommand(self, device, self.instance)}
        write('Get WBEM Instance %s from %s' % (queries['test'], device.id))
        write('')
        start = time.time()
        try:
            cn, kb, ns = self.getInstanceName(device)
            url = 'http%s://%s:%s' % (device.zWbemUseSSL is True and 's' or '',
                                            device.manageIp, device.zWbemPort)
            creds = (device.zWinUser, device.zWinPassword)
            conn = pywbem.WBEMConnection(url,creds)
            if kb:
                instanceName = pywbem.CIMInstanceName(  cn,
                                                        keybindings=kb,
                                                        namespace=ns)
                instance = conn.GetInstance(instanceName,
                                            includeQualifiers=True,
                                            localOnly=False)
                for property in instance.items():
                    write('%s = %s' % (property[0], property[1]))
            else:
                instance = conn.EnumerateInstanceNames( cn, namespace=ns)
                for property in instance:
                    write('%s' % property)
        except:
            import sys
            write('exception while executing command')
            write('type: %s  value: %s' % tuple(sys.exc_info()[:2]))
        write('')
        write('')
        write('DONE in %s seconds' % long(time.time() - start))
        out.write(str(footer))
