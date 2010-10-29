#!/usr/bin/env python
"""Start the jabber bot and load our plugins"""

import Globals
import sys
import os, glob
import transaction

from Jabber.Adapter import TwistedJabberClient
from Jabber.Plugins import initPluginSystem, findPlugins

HAVE_SSL = False
try:
    from twisted.internet import ssl
    HAVE_SSL = True
except ImportError:
    ssl = None

from Products.ZenUtils.ZCmdBase import ZCmdBase
from Products.ZenHub.PBDaemon import PBDaemon 
from Products.ZenEvents.zenactions import *

class XmppBot(ZenActions, ZCmdBase, PBDaemon):

    def buildOptions(self):
        ZCmdBase.buildOptions(self)
        self.parser.add_option( '--jabber_pass', dest='jabber_pass', type='string', help='Password used to connect to the XMPP server')
        self.parser.add_option( '--jabber_user', dest='jabber_user', type='string', help='Username used to connect to the XMPP server')
        self.parser.add_option( '--jabber_host', dest='jabber_host', type='string', default='localhost', help='(OPTIONAL) XMPP server to connect')
        self.parser.add_option( '--jabber_port', dest='jabber_port', type='int', help='(OPTIONAL) Port used to connect to the XMPP server')
        self.parser.add_option( '--first_user', dest='first_user', type='string', help='User mapping to bootstrap the bot with at least on authorized user.  Example specification myzenossname,myjabberid@server.example.com')
        self.parser.add_option( '--resource', dest='resource', type='string', default='xmppbot', help='(OPTIONAL) jabber resource name.')
        self.parser.add_option( '--im_host', dest='im_host', type='string', help='(OPTIONAL) option for addressing IM users when the server is not known.  If this is ommitted, jabber_host will be used.')
        self.parser.add_option( '--ssl', dest='ssl', action='store_true', help='(OPTIONAL) ssl.')
        self.parser.add_option( '--group_server', type='string', dest='group_server', help='(OPTIONAL) Conference/groupchat server.  If the name has no dots, it will use group_server.jabber_host')
        self.parser.add_option( '--chatrooms', dest='chatrooms', action='append', type='string', help='(OPTIONAL) First chatroom joined to when connecting.  May be specified multiple times to join multiple rooms.')
        self.parser.add_option('--cycletime', dest='cycletime', default=60, type='int', help='(OPTIONAL) check events every cycletime seconds')
        self.parser.add_option( '--zopeurl', type='string', dest='zopeurl', default='http://%s:%d' % (socket.getfqdn(), 8080), help='(OPTIONAL) http path to the root of the zope server')
        self.parser.add_option('--monitor', type='string', dest='monitor', default=DEFAULT_MONITOR, help='(OPTIONAL) Name of monitor instance to use for heartbeat events. Default is %s.' % DEFAULT_MONITOR)

    def __init__(self):
        PBDaemon.__init__(self, keeproot=True)
        ZCmdBase.__init__(self)

        wants_ssl = self.options.ssl
        if wants_ssl and not HAVE_SSL:
            self.log.error('SSL was requested for Jabber connection, but pyopenssl is not installed.  Please install it and start the xmppBot again.')
            sys.exit(2)

        if not self.options.jabber_pass:
            self.log.error('--jabber_pass is required')
            sys.exit(2)

        if not self.options.jabber_user:
            self.log.error('--jabber_user is required')
            sys.exit(2)

        if self.options.first_user:
            try:
                zenUser, jabberId = self.options.first_user.split(',')
            except ValueError:
                self.log.error('--first_user option must contain both zenuser and jabberid separated by a comma.  Example: chudler,chudler@im.example.com')
                sys.exit(2)

            if zenUser and jabberId:
                self.setFirstUser(zenUser, jabberId)
            else:
                self.log.error('--first_user option must contain both zenuser and jabberid separated by a comma.  Example: chudler,chudler@im.example.com')
                sys.exit(2)

        # taken from zenactions.py
        self.schedule = Schedule(self.options, self.dmd)
        self.actions = []
        self.loadActionRules()
        self.updateCheck = UpdateCheck()

        self.sendEvent(Event.Event(device=self.options.monitor,
        eventClass=App_Start, summary='Jabber Bot started', severity=0, component='xmppbot'))

        password = self.options.jabber_pass
        chatrooms = self.options.chatrooms
        username = self.options.jabber_user
        server = self.options.jabber_host
        port = self.options.jabber_port
        groupServer = self.options.group_server
        realHost = self.options.im_host
        resource = self.options.resource

        self.client = TwistedJabberClient(server=server, username=username, password=password,
                                 port=port,
                                 groupServer=groupServer,
                                 chatrooms=chatrooms, ssl=wants_ssl,
                                 realHost=realHost, resource=resource)

        path = os.path.realpath(sys.argv[0])
        pluginPath = os.path.dirname(path) + '/Jabber/plugins'
        self.log.info("xmppBot plugins will be loaded from %s" % pluginPath)

        plugins = [pluginFile.split('/')[-1].split('.py')[0] for pluginFile in glob.glob( os.path.join(pluginPath, '*.py') )]

        self.log.debug("xmppBot loading pugins  %s" % ', '.join(plugins))
        initPluginSystem(pluginPath=pluginPath, plugins=plugins, jabberClient=self.client)

        # connect to the jabber server
        self.log.info('Connecting to server')
        reactor = self.client.connect()

        # begin looking for zenevents
        self.schedule.start()
        self.runCycle()

        reactor.suggestThreadPoolSize(10)
        reactor.run()

    def setFirstUser(self, zenUser, jabberId):
        zenUser = zenUser.lower()
        haveUser = False
        for user in  self.dmd.ZenUsers.getAllUserSettings():
            if user.id.lower() == zenUser:
                haveUser = True
                user._updateProperty('JabberId', jabberId)
                transaction.commit()
                break
        return haveUser

    # ripped from zenactions.py
    def mainbody(self):
        """main loop to run actions.
        """
        from twisted.internet.process import reapAllProcesses
        reapAllProcesses()
        zem = self.dmd.ZenEventManager
        self.loadActionRules()
        self.processRules(zem)

    # ripped from zenactions.py
    def runCycle(self):
        try:
            start = time.time()
            self.syncdb()
            self.mainbody()
            self.log.info('processed %s rules in %.2f secs', len(self.actions), time.time()-start)
        except:
            self.log.exception('unexpected exception')
        reactor.callLater(60, self.runCycle)

    # ripped from zenactions.py
    def loadActionRules(self):
        self.actions = []
        for ar in self.dmd.ZenUsers.getAllActionRules():
            if not ar.enabled: continue
            if not ar.action.title() == 'Xmpp': continue
            userid = ar.getUser().id
            self.actions.append(ar)
            self.log.debug('action:%s for:%s loaded', ar.getId(), userid)

    # ripped from zenactions.py
    def sendHeartbeat(self):
        """Send a heartbeat event for this monitor.
        """
        timeout = self.options.cycletime*3
        evt = Event.EventHeartbeat(self.options.monitor, 'xmppbot', timeout)
        self.sendEvent(evt)
        self.niceDoggie(self.options.cycletime)

    # zenactions will call sendXmpp when an event comes in that the user wants
    # to see.
    def sendXmpp(self, action, data, clear = None):
        message, body = self.format(action, data, clear)
        recipients = self.getAddress(action)
        if not recipients:
            self.log.warning('failed to send message %s on rule %s: %s', action.getUser().id, action.id, 'Unspecified recipient.')
            return True
        for recipient in recipients:
            self.log.debug('Sending message to %s: %s', recipient, message)
            if recipient.lower().endswith('/groupchat'):
                messageType = 'groupchat'
            else:
                messageType = 'chat'
            self.client.sendMessage(message, recipient, messageType)
            return True

    def getAddress(self, action):
        if action.targetAddr:
            return [action.targetAddr]
        else:
            results = []
            zenUser = action.getUser()
            # attempt to detect a group and resolve its users, otherwise see if it is a user
            if 'getMemberUserIds' in dir(zenUser):
                for username in zenUser.getMemberUserIds():
                    try:
                        results.append(zenUser.getUserSettings(username).getProperty('JabberId').strip())
                    except None:
                        self.log.error('Unable to send xmpp alert message to %s.  This might happen if they are missing the jabberId property.  Try the bot command "setjid"' % username)

            # getEmailAddresses should at least identify an entity that would have a jabberId on it, unless it was a group (above)
            elif 'getEmailAddresses' in dir(zenUser):
                try:
                    results.append(zenUser.getProperty('JabberId').lower())
                except None:
                    self.log.error('Unable to send xmpp alert message to %s.  This might happen if they are missing the jabberId property.  Try the bot command "setjid"' % zenUser)
            else:
                self.log.error('Unable to send xmpp alert message to %s.  Please report this error to the author of this plugin' % zenUser)

            return results

if __name__ == '__main__':
    import logging
    logging.getLogger('zen.Events').setLevel(80)
    bot = XmppBot()
