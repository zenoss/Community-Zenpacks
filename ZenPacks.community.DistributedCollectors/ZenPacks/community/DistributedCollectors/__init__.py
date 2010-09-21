################################################################################
#
# This program is part of the DistributedCollectors Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

import Globals
import os
import socket
import cgi
import time
import transaction

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenWidgets import messaging
from Products.ZenUtils.Utils import monkeypatch, zenPath, binPath, executeCommand
from Products.ZenUtils.Utils import executeStreamCommand
from Products.ZenModel.PerformanceConf import performancePath
from Products.ZenModel.ZVersion import VERSION

zpDir = zenPath('ZenPacks')
updConfZenBin = zenPath('bin/updateConfigs')
updConfBin = os.path.join(os.path.dirname(__file__), 'bin/updateConfigs')
masterdaemons=['zeoctl','zopectl','zenhub','zenjobs','zenactions','zenmodeler']


class blackhole:
    def write(self, text=None):
        return

def setupRemoteMonitors(ids, templ, REQUEST=None, install=None, remove=None):
    if REQUEST and VERSION < '2.6':
        out = REQUEST.RESPONSE
    else: out = blackhole()
    def write(lines):
        ''' Output (maybe partial) result text.
        '''
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

    header, footer = templ.split('OUTPUT_TOKEN')
    out.write(str(header))
    for id in ids:
        write('Remote Collector %s'%id)
        write('Stopping zenoss daemons')
        executeStreamCommand('ssh %s "zenoss stop"'%id, write, timeout=240)
        if remove:
            write('Revert Remote Collector configuration')
            executeStreamCommand('ssh %s %s localhost localhost'%(id,
                                            updConfZenBin), write, timeout=240)
        write('Remove ZenPacks files from Remote Collector')
        executeStreamCommand('ssh %s rm -fr %s'%(id, zpDir), write, timeout=240)
        if install:
            write('Copy ZenPacks files to Remote Collector')
#  Copy ZenPacks files with scp
#            executeStreamCommand('scp -r %s %s:%s'%(zpDir, id, zpDir), write,
#                                                                timeout=240)
#  Copy ZenPacks files with cpio compression
            executeStreamCommand('find %s -print | cpio -oc | ssh -C %s "cd / && cpio -ic 2>/dev/null"'%(
                                            zpDir, id), write, timeout=240)
            write('Update Remote Collector configuration')
            executeStreamCommand('ssh %s %s %s %s'%(id, updConfBin,
                                    socket.getfqdn(), id), write, timeout=240)
        write('Starting zenoss daemons')
        executeStreamCommand('ssh %s "zenoss start"'%id, write, timeout=240)
        write('Finish')
    out.write(str(footer))


@monkeypatch('Products.ZenModel.Device.Device')
def setPerformanceMonitor(self, performanceMonitor,
                            newPerformanceMonitor=None, REQUEST=None):
    """
    Set the performance monitor for this device.
    If newPerformanceMonitor is passed in create it

    @permission: ZEN_CHANGE_DEVICE
    """
    if newPerformanceMonitor:
        #self.dmd.RenderServer.moveRRDFiles(self.id,
        #    newPerformanceMonitor, performanceMonitor, REQUEST)
        performanceMonitor = newPerformanceMonitor

    obj = self.getDmdRoot("Monitors").getPerformanceMonitor(
                                                    performanceMonitor)
    try:
        if self.getPerformanceServerName() == performanceMonitor: raise
        if self.getPerformanceServer().renderurl == '/zport/RenderServer':
            self.dmd.RenderServer.packageRRDFiles(self.id)
            self.dmd.RenderServer.deleteRRDFiles(self.id)
        else:
            os.system('ssh %s tar -C%s -czf - . > %s/%s.tgz'%(
                                    self.getPerformanceServer().id,
                                    performancePath('/Devices/%s'%self.id),
                                    self.dmd.RenderServer.tmpdir, self.id))
            os.system('ssh %s rm -fr %s'%(self.getPerformanceServer().id,
                                    performancePath('/Devices/%s'%self.id)))
        if obj.renderurl == '/zport/RenderServer':
            self.dmd.RenderServer.unpackageRRDFiles(self.id)
        else:
            os.system('cat %s/%s.tgz | ssh %s "(mkdir -p %s && tar -C%s -xzf - )"'%(
                                    self.dmd.RenderServer.tmpdir,self.id,obj.id,
                                    performancePath('/Devices/%s'%self.id),
                                    performancePath('/Devices/%s'%self.id)))
        os.unlink('%s/%s.tgz'%(self.dmd.RenderServer.tmpdir, self.id))
    except:
        pass
    self.addRelation("perfServer", obj)
    self.setLastChange()

    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Monitor Changed',
            'Performance monitor has been set to %s.' % performanceMonitor
        )
        return self.callZenScreen(REQUEST)

@monkeypatch('Products.ZenModel.MonitorClass.MonitorClass')
def manage_addRemoteMonitor(self, id, submon=None, REQUEST=None):
    'Add an object of sub_class, from a module of the same name'
    self.manage_addMonitor(id, submon, None)
    transaction.commit()
    daemons = open('%s/daemons.txt'%zpDir, 'w')
    for daemon in self.dmd.About.getZenossDaemonStates():
        if daemon['msg'] != 'Up': continue
        if daemon['name'] in masterdaemons: continue 
        daemons.write('%s\n'%daemon['name'])
    daemons.close()
    setupRemoteMonitors([id,], self.commandTestOutput(), REQUEST, install=True)
    os.unlink('%s/daemons.txt'%zpDir)
    self.dmd.Monitors.Performance[id].renderurl='http://%s:8091' % id
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Remote Collector Created',
            'Remote collector %s was created.' % id
        )
        return self.callZenScreen(REQUEST)


@monkeypatch('Products.ZenModel.MonitorClass.MonitorClass')
def manage_updateRemoteMonitors(self, ids=None, submon="", REQUEST=None):
    'Update an object from this one'
    daemons = open('%s/daemons.txt'%zpDir, 'w')
    for daemon in self.dmd.About.getZenossDaemonStates():
        if daemon['msg'] != 'Up': continue
        if daemon['name'] in masterdaemons: continue 
        daemons.write('%s\n'%daemon['name'])
    daemons.close()
    setupRemoteMonitors(ids, self.commandTestOutput(), REQUEST, install=True, remove=True)
    os.unlink('%s/daemons.txt'%zpDir)
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Remote Collectors Updated',
            'Updated remote collectors: %s' % (', '.join(ids))
        )
        return self.callZenScreen(REQUEST)

@monkeypatch('Products.ZenModel.MonitorClass.MonitorClass')
def manage_removeRemoteMonitors(self, ids=None, submon="", REQUEST=None):
    'Remove an object from this one'
    self.manage_removeMonitor(ids, submon, None)
    transaction.commit()
    setupRemoteMonitors(ids, self.commandTestOutput(), REQUEST, remove=True)
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Remote Collectors Deleted',
            'Deleted remote collectors: %s' % (', '.join(ids))
        )
        return self.callZenScreen(REQUEST)

@monkeypatch('Products.ZenModel.PerformanceConf.PerformanceConf')
def _executeZenModelerCommand(self, zenmodelerOpts, REQUEST=None):
    """
    Execute zenmodeler and return result
    
    @param zenmodelerOpts: zenmodeler command-line options
    @type zenmodelerOpts: string
    @param REQUEST: Zope REQUEST object
    @type REQUEST: Zope REQUEST object
    @return: results of command
    @rtype: string
    """
    zm = binPath('zenmodeler')
    zenmodelerCmd = [zm]
    zenmodelerCmd.extend(zenmodelerOpts)
    if zenmodelerOpts[3] != 'localhost':
        zenmodelerCmd.extend(['--hubhost', socket.getfqdn()])
        zenmodelerCmd = ['/usr/bin/ssh', zenmodelerOpts[3]] + zenmodelerCmd
    result = executeCommand(zenmodelerCmd, REQUEST)
    return result

@monkeypatch('Products.ZenModel.PerformanceConf.PerformanceConf')
def _executeZenDiscCommand(self, deviceName, devicePath= "/Discovered", 
                      performanceMonitor="localhost", discoverProto="snmp",
                      zSnmpPort=161,zSnmpCommunity="", REQUEST=None):
    """
    Execute zendisc on the new device and return result
    
    @param deviceName: Name of a device
    @type deviceName: string
    @param devicePath: DMD path to create the new device in
    @type devicePath: string
    @param performanceMonitor: DMD object that collects from a device
    @type performanceMonitor: DMD object
    @param discoverProto: auto or none
    @type discoverProto: string
    @param zSnmpPort: zSnmpPort
    @type zSnmpPort: string
    @param zSnmpCommunity: SNMP community string
    @type zSnmpCommunity: string
    @param REQUEST: Zope REQUEST object
    @type REQUEST: Zope REQUEST object
    @return:
    @rtype:
    """
    zm = binPath('zendisc')
    zendiscCmd = [zm]
    zendiscOptions = ['run', '--now','-d', deviceName,
                     '--monitor', performanceMonitor, 
                     '--deviceclass', devicePath]
    if REQUEST: 
        zendiscOptions.append("--weblog")
    zendiscCmd.extend(zendiscOptions)
    if performanceMonitor != 'localhost':
        zendiscCmd.extend(['--hubhost', socket.getfqdn()])
        zendiscCmd = ['/usr/bin/ssh', performanceMonitor] + zendiscCmd
    result = executeCommand(zendiscCmd, REQUEST)
    return result

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.ZenMenu import ZenMenu

class ZenPack(ZenPackBase):
    def install(self, app):
        self.replaceString(zenPath('bin/zenoss'),'	#C="$C zenrender"','	C="$C zenrender"')
        if os.path.exists(zenPath('etc/DAEMONS_TXT_ONLY')) and os.path.exists(zenPath('etc/daemons.txt')):
            self.replaceString(zenPath('etc/daemons.txt'),'','zenrender')
        ZenPackBase.install(self, app)
        self.installMenuItems(app.zport.dmd)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self.installMenuItems(app.zport.dmd)

    def remove(self, app, leaveObjects=False):
        self.replaceString(zenPath('bin/zenoss'),'	C="$C zenrender"','	#C="$C zenrender"')
        if os.path.exists(zenPath('etc/DAEMONS_TXT_ONLY')) and os.path.exists(zenPath('etc/daemons.txt')):
            self.replaceString(zenPath('etc/daemons.txt'),'zenrender','')
        self.removeMenuItems(app.zport.dmd)
        ZenPackBase.remove(self, app, leaveObjects)

    def installMenuItems(self, dmd):
        self.removeMenuItems(dmd)
        menu = dmd.zenMenus.PerformanceMonitor_list
        menu.manage_addZenMenuItem(
            "addRPMonitor",
            action="dialog_addRemoteMonitor",
            description="Add Remote Monitor...",
            isdialog=True,
            permissions=('Manage DMD',),
            ordering=70.0)
        menu.manage_addZenMenuItem(
            "updateRPMonitor",
            action="dialog_updateRemoteMonitors",
            description="Update Remote Monitors...",
            isdialog=True,
            permissions=('Manage DMD',),
            ordering=60.0)
        menu.manage_addZenMenuItem(
            "removeRPMonitor",
            action="dialog_removeRemoteMonitors",
            description="Delete Remote Monitors...",
            isdialog=True,
            permissions=('Manage DMD',),
            ordering=50.0)

    def removeMenuItems(self, dmd):
        menu = dmd.zenMenus.PerformanceMonitor_list
        items = []
        for i in ["addRPMonitor", "updateRPMonitor", "removeRPMonitor"]:
            if hasattr(menu.zenMenuItems, i): items.append(i)
        if len(items) > 0: menu.manage_deleteZenMenuItem(tuple(items))

    def replaceString(self, path, search, repl):
        import fileinput
        for line in fileinput.input(path, inplace=1):
            if search != '': newline = line.strip('\n').replace(search, repl) 
            elif fileinput.lineno() == 4: newline = "%s\n%s"(line.strip('\n'), repl)
            else: newline = line.strip('\n')
            if repl == newline == '' and  line.strip('\n') != '':continue
            print newline
