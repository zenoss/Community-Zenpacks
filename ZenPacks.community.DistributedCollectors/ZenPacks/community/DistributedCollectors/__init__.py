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
from Products.ZenUtils.Utils import monkeypatch
from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.Utils import executeStreamCommand

zpDir = zenPath('ZenPacks')
updConfBin = os.path.join(os.path.dirname(__file__), 'bin/updateConfigs')
masterdaemons=['zeoctl','zopectl','zenhub','zenjobs','zenactions','zenmodeler']


def setupRemoteMonitors(ids, templ, REQUEST=None, install=None, remove=None):
    if REQUEST:
        out = REQUEST.RESPONSE
    else: out = None
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
                                                updConfBin), write, timeout=240)
        write('Remove ZenPacks files from Remote Collector')
        executeStreamCommand('ssh %s rm -fr %s'%(id, zpDir), write, timeout=240)
        if install:
            write('Copy ZenPacks files to Remote Collector')
#  Copy ZenPacks files with scp
#            executeStreamCommand('scp -r %s %s:%s'%(zpDir, id, zpDir), write,
#
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


@monkeypatch('Products.ZenModel.MonitorClass.MonitorClass')
def manage_addRemoteMonitor(self, id, submon=None, REQUEST=None):
    'Add an object of sub_class, from a module of the same name'
    self.manage_addMonitor(id, submon)
    transaction.commit()
    daemons = open('%s/daemons.txt'%zpDir, 'w')
    for daemon in self.dmd.About.getZenossDaemonStates():
        if daemon['msg'] != 'Up': continue
        if daemon['name'] in masterdaemons: continue 
        daemons.write('%s\n'%daemon['name'])
    daemons.close()
    setupRemoteMonitors([id,], self.commandTestOutput(), REQUEST, install=True)
    os.unlink('%s/daemons.txt'%zpDir)
    self.dmd.Monitors.Performance[id].renderurl='http://%s:8090/%s'%(socket.getfqdn(),id)
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Monitor Created',
            'Monitor %s was created.' % id
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
            'Monitors Updated'
            'Updated monitors: %s' % (', '.join(ids))
        )
        return self.callZenScreen(REQUEST)

@monkeypatch('Products.ZenModel.MonitorClass.MonitorClass')
def manage_removeRemoteMonitors(self, ids=None, submon="", REQUEST=None):
    'Remove an object from this one'
    self.manage_removeMonitor(ids, submon)
    transaction.commit()
    setupRemoteMonitors(ids, self.commandTestOutput(), REQUEST, remove=True)
    if REQUEST:
        messaging.IMessageSender(self).sendToBrowser(
            'Monitors Deleted',
            'Deleted monitors: %s' % (', '.join(ids))
        )
        return self.callZenScreen(REQUEST)


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
