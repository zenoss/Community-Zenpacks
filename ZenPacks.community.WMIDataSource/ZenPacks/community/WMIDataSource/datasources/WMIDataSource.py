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

$Id: WMIDataSource.py,v 1.2 2009/12/20 13:51:23 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel import RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenUtils.Utils import executeStreamCommand
from AccessControl import ClassSecurityInfo, Permissions

import cgi, time
import os

class WMIDataSource(ZenPackPersistence, RRDDataSource.RRDDataSource):

    ZENPACKID = 'ZenPacks.community.WMIDataSource'

    sourcetypes = ('WMI',)
    sourcetype = 'WMI'
    namespace = 'root/cimv2'
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
            self.wql = REQUEST.get('wql', '')
        return RRDDataSource.RRDDataSource.zmanage_editProperties(
                                                                self, REQUEST)

    def getInstanceInfo(self, context):
        instance = RRDDataSource.RRDDataSource.getCommand(self, context,
                                                            self.wql)
        namespace = RRDDataSource.RRDDataSource.getCommand(self, context,
                                            self.namespace).replace("\\", "/")
        if instance.upper().startswith('SELECT '):
            return ('WMI', instance, 'WQL', namespace)
        classname = instance.split('.', 1)
	if len(classname) < 2:
            return ('WMI', instance, None, namespace)
        keybindings = {}
        for key in classname[1].split(','):
            var, val = key.split('=')
            keybindings[var] = val.strip('"')
        return ('WMI', classname[0], keybindings, namespace)


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

        start = time.time()
        try:
            tr, inst, kb, namespace = self.getInstanceInfo(device)
            inst = RRDDataSource.RRDDataSource.getCommand(self, device,
                                                            self.wql)
	    properties = dict([(
	                dp.getAliasNames() and dp.getAliasNames()[0] or dp.id,
			dp.id) for dp in self.getRRDDataPoints()])
            url = '//%%s%s/%s'%(device.zWmiProxy or device.manageIp, namespace)
            write('Get %s Instance %s from %s' % (tr, inst, str(url%'')))
            write('')
            creds = '%s:%s@'%(device.zWinUser, device.zWinPassword)
            zp = self.dmd.ZenPackManager.packs._getOb(
                                   'ZenPacks.community.%sDataSource'%tr, None)
            command = "python %s -c \"%s\" -q \"%s\" -f \"%s\" -a \"%s\""%(
                                                zp.path('%sClient.py'%tr),
                                                str(url%creds),
                                                inst,
                                                " ".join(properties.keys()),
						" ".join(properties.values()))
            executeStreamCommand(command, write)
        except:
            import sys
            write('exception while executing command')
            write('type: %s  value: %s' % tuple(sys.exc_info()[:2]))
        write('')
        write('')
        write('DONE in %s seconds' % long(time.time() - start))
        out.write(str(footer))
