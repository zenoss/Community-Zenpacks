#!/usr/bin/python
"""jabber bot"""
# TODO:
# * fix notification about ivalid messages when direct-chatting

import logging
import re
import StringIO, csv
import random

try:
    from twisted.internet import ssl
except ImportError:
    pass

from twisted.words.protocols.jabber import client, jid
from twisted.words.xish import domish
from twisted.internet import reactor
from Plugins import getPluginsByCapability
from twisted.internet.task import LoopingCall

JABBER_CLIENT_NS = 'jabber:client'

class TwistedJabberClient:

    def __init__(self, server, username, password,
                 groupServer, chatrooms, ssl, realHost, resource, port = None):
        self.server = server
        self.ssl = ssl

        if not port:
            if self.ssl:
                self.port = 5223
            else:
                self.port = 5222
        else:
            self.port = int(port)

        self.username = username
        self.password = password
        self.resource = resource

        self.mute = False

        self._send = None

        if not isinstance(chatrooms, list):
            chatrooms = [ chatrooms ]
        self.chatrooms = chatrooms
        self._waitingRoster = False

        self.logger = logging.getLogger('zen.xmppBot')
        self.pluginLogger = logging.getLogger('zen.xmppBot.plugins')
        self.logger.setLevel(10)
        self.pluginLogger.setLevel(10)

        if realHost:
            self.realHost = realHost
        else:
            self.realHost = self.server

        if groupServer:
            if '.' in groupServer:
                self.groupServer = groupServer
            else:
                self.groupServer = '%s.%s' % (groupServer, self.realHost)
        else:
            self.groupServer = 'conference.%s' % self.realHost

        self.myJid = self.jidString(self.username)


    def connect(self):
        """connect to the jabber server"""
        self.logger.debug('Starting to connect')
        self.logger.debug('Building context factory for jid %s' % self.myJid)
        factory = client.basicClientFactory(jid.JID(self.myJid), self.password)
        factory.addBootstrap('//event/stream/authd', self.authenticate)

        self.logger.debug('Connecting to server %s (port %d) using id %s...' % (self.server, self.port, self.myJid))
        if self.ssl:

            class contextFactory:
                isClient = 1
                method = ssl.SSL.SSLv3_METHOD

                def getContext(self):
                    context = ssl.SSL.Context(self.method)
                    return context

            self.logger.debug('Connecting with ssl...')
            reactor.connectSSL(self.server, self.port, factory, contextFactory())
        else:
            reactor.connectTCP(self.server, self.port, factory)
        return reactor

    def jidString(self, user, conference = False, resource = True):
        """make and return a Jabber identifier (jid) for a user's nick.

        if conf is a non empty string, use this string as the conference room
        and go through the conference server

        if resource is true, append the resource to the jid
        """

        result = user

        if conference:
            if '@' not in conference:
                result = '%s@%s/%s' % (conference, self.groupServer, user)
        elif '@' not in user:
            result = '%s@%s' % (user, self.realHost)

        if resource:
            result += '/%s' % self.resource

        return result

    def authenticate(self, twistedStanza):
        """authentication callback"""

        self._send = twistedStanza.send

        # add observers for incoming message / presence requests
        #twistedStanza.addObserver('/iq',       self.iqHandler)
        #twistedStanza.addObserver('/presence', self.dialogHandler.presenceHandler)
        twistedStanza.addObserver('/presence', self.presenceHandler)
        twistedStanza.addObserver('//event/stream/error', self.streamErrorHandler)
        #twistedStanza.addObserver('//event/stream/error', self.streamErrorHandler)

        #twistedStanza.addObserver('/message',  self.dialogHandler.messageHandler)
        twistedStanza.addObserver('/message',  self.messageHandler)

        self.requestRoster()

        # let'em know we are online
        presence = domish.Element((JABBER_CLIENT_NS, 'presence'))
        presence.addElement('status').addContent('Online')
        self.send(presence)

        keepalive = LoopingCall(self.loopEntry)
        keepalive.start(60)

        self.joinChatrooms(self.chatrooms)

    def loopEntry(self):
        """Periodic actions that need to be taken independent of jabber activity"""
        # let the server know we are still here
        self.keepAlive()
        self.processAlerts()

    def joinChatrooms(self, chatrooms = ()):
        """Join the chatrooms given in +chatrooms+ argument"""
        # coerce chatrooms into iterable or obtain the iterator
        rooms = getattr(chatrooms, '__iter__', getattr((chatrooms,), '__iter__')) 
        for roomName in rooms():
            self.logger.debug('Username %s will join %s.' % (self.username, roomName))
            roomJid = self.jidString(self.username, roomName, False)
            self.logger.debug('Joining %s MUC.' % roomJid)
            self.send(self.presenceElement(self.myJid, roomJid))

    def presenceElement(self, from_, to, presenceType=None):
        """create and return an xml presence element"""
        twistedStanza = domish.Element((JABBER_CLIENT_NS, 'presence'))
        twistedStanza['from'] = from_
        twistedStanza['to'] = to
        if presenceType:
            twistedStanza['type'] = presenceType
        return twistedStanza

    def keepAlive(self):
        """Send a iq ping to the server.  Used as a keepalive."""
        iqPing = domish.Element((JABBER_CLIENT_NS, 'iq'))
        iqPing['type'] = 'get'
        iqPing['id'] = 'fmb222_' + str(random.randrange(1000000))
        iqPing.addElement(('urn:xmpp:ping', 'ping'))
        self.logger.debug('SENDING PING %s' % iqPing)
        self.send(iqPing)

    def processAlerts(self):
        """this is called periodically by LoopingCall to wake up the plugins that are not driven by user input"""
        for plugin in getPluginsByCapability('alert', self):
            self.logger.debug('Calling alert plugin %s' % plugin)
            reactor.callInThread(plugin.alert, client=self, log=self.pluginLogger)

    def presenceHandler(self, twistedStanza):
        """handle a presence packet and take action on it if necessary"""
        self.logger.debug('-< received %s' % twistedStanza.toXml())
        self.logger.debug('Checking presence access for %s' % twistedStanza['from'])
        sender = self.checkAccess(twistedStanza['from'], 'presence')
        if sender:
            messageType = twistedStanza.attributes.get('type', 'nothing')
            if messageType == 'subscribe':
                self.send(self.presenceElement(self.jidString(self.username), sender, 'subscribed'))

    def streamErrorHandler(self, twistedStanza):
        """handle an error"""
        self.logger.debug('-< received %s' % twistedStanza.toXml())

    def shouldDrop(self, twistedStanza):
        """ignore delayed messages or error messages"""
        for element in twistedStanza.elements():
            if element.uri == 'jabber:x:delay':
                self.logger.debug('*** should drop delayed msg %s' % twistedStanza.toXml())
                return True
            elif element.getAttribute('type') == 'error':
                self.logger.debug('*** should drop ERROR msg %s' % twistedStanza.toXml())
                return True

    def messageHandler(self, twistedStanza):
        """handle a message packet and take appropriate action"""

        if self.shouldDrop(twistedStanza):
            self.logger.debug('*** dropping the message')
            return

        self.logger.debug('-< received %s' % twistedStanza.toXml())
        fromJid = twistedStanza['from']
        messageType = twistedStanza.attributes.get('type', 'nothing')
        self.logger.debug('Checking message type %s access control for %s' % (messageType, fromJid))

        if not self.checkAccess(fromJid, messageType): return

        if '/' not in fromJid:
            for element in twistedStanza.elements():
                self.logger.debug("ELEMENT %s" % element)
                if element.uri == 'jabber:x:conference':
                    self.checkInvite(twistedStanza)
                    return
            self.logger.debug('*** dropping message from %s (no resource set)' % fromJid)
            return

        if fromJid.split('/', 1)[1] == self.username:
            self.logger.debug('*** dropping request from %s, is self' % fromJid)
            return

        self.checkCommand(twistedStanza)

    def checkCommand(self, twistedStanza):
        """Check the message for a command and dispatch it if it contains one"""
        fromJid = twistedStanza['from']
        messageType = twistedStanza.attributes.get('type', 'nothing')
        for element in twistedStanza.elements():
            if element.name == 'body':
                self.logger.debug('Processing chat FROm:%s BODy:%s' % (fromJid, element.toXml()))
                try:
                    message = element.children[0]
                except IndexError:
                    continue
                command = self.findCommand(message, messageType)
                room = fromJid.split('@', 1)[0]
                self.logger.debug('RETURNED command "%s"' % command)
                if command:
                    self.dispatchCommand(command, fromJid,  message,
                                         twistedStanza, room, messageType)
                else:
                    for plugin in getPluginsByCapability('default', self):
                        self.logger.debug('Calling default plugin %s sender:%s, room:%s, message:%s' % (plugin, fromJid, room, message))
                        plugin.default(client = self, message = message, sender = fromJid,
                                       room = room, twistedStanza = twistedStanza, log = self.pluginLogger)
                break

    def findCommand(self, message, messageType):
        """Take the message body and return a dict of its parts for command dispatching"""
        self.logger.debug('Checking message %s' % message)
        commandPart = None

        if '!.' in message:
            _, _, commandPart = message.partition('!.')
        elif self.username in message:
            _, _, commandPart = message.partition('%s:' % self.username)
        elif messageType == 'chat':
            commandPart = message
            self.logger.debug('A command came in from a NON-MUC without command key sequence %s' % commandPart)
        self.logger.debug('Found command "%s" from message "%s"' % (commandPart, message))
        if commandPart:
            self.logger.debug('Found command "%s" from message "%s"' % (commandPart, message))
            return self.getListOfTokens(commandPart.strip())

    def dispatchCommand(self, command, sender, originalMessage, twistedStanza, room, messageType):
        """Find plugins that can respond to the command or execute all the plugins responding to default"""
        self.logger.debug('Dispatching command %s' % command)
        """Command is meant for the bot"""
        self.logger.debug('This is our command')
        plg = command.pop(0).lower()
        args = []
        for arg in command:
            args.append(arg.strip())
        message = ''
        """Handle a few high level commands: help, mute, unmute"""
        if plg == 'help':
            self.logger.debug('Finding plugins with help')
            message = 'In a groupchat, all commands start with "%s:" or "!."\nIn private chat, simply type the command.\nThese are the commands available.  For help on a command, try -h\n' % self.username
            pluginNames = []
            for plugin in getPluginsByCapability('help', self):
                self.logger.debug('plugins %s has help' % plugin)
                try:
                    pluginNames.append(plugin.name)
                except AttributeError:
                    # baaad plugin, doesn't assign a name for itself
                    pass
            message += ', '.join(pluginNames)
            self.sendMessage(message, sender, messageType)
            return
        if plg == 'default':
            # this is necessary to prevent users from invoking the catchall (default) plugins
            self.sendMessage('Unknown command.  Try help.', sender, messageType)
        else:
            # find the plugins having the command name
            plugin_arguments = { 'args':args, 'command':'something', 'client':self,
                               'message':originalMessage, 'messageType':messageType,
                               'sender':sender, 'twxml':twistedStanza,
                               'room':room, 'log':self.pluginLogger }
            foundCommand = False
            for plugin in getPluginsByCapability(plg, self):
                if not plugin.private:
                    foundCommand = True
                    self.logger.debug('Calling plugin %s with %s' % (plg, plugin_arguments))

                    plugin_arguments['command'] = plg

                    if plugin.threadsafe:
                        self.logger.debug('%s is marked as threadsafe' % plg)
                        reactor.callInThread(plugin.call, **plugin_arguments)
                    else:
                        plugin.call(**plugin_arguments)

                else:
                    self.logger.debug('Would have called plugins %s, but it is private' % plg)

            if not foundCommand:
                self.sendMessage('Unknown command.  Try help.', sender, messageType)

    # TODO:
    # -check if user is the room already if inviting
    # -check if client supports the feature using iq: http://xmpp.org/extensions/xep-0249.html#support
    # -assembling all stanzas separately seems dumb, maybe fix

    def assembleInvite(self, message, to, room):
        self.logger.debug('Assembling invite to: %s' % (to)) 
        twistedStanza = domish.Element((JABBER_CLIENT_NS, 'message'))
        twistedStanza['from'] = self.jidString(self.username)
        twistedStanza['to'] = to
        x = domish.Element(('jabber:x:conference','x'))
        x['jid'] = room
        x.addElement('reason', content = message)
        twistedStanza.addChild(x)
        return twistedStanza

    def sendInvite(self, message, to, room):
        if not self.mute:
            msgStanza = self.assembleInvite(message, to, room)
            self.send(msgStanza)

    def assembleMessage(self, message, to, messageType):
        """create and return an xml message element"""
        self.logger.debug('Assembling message to: %s of type: %s' % (to, messageType)) 
        twistedStanza = domish.Element((JABBER_CLIENT_NS, 'message'))
        inForum = None
        if self.fromRoom(to) :
            inForum = to.split('@', 1)[0]
            if messageType.lower() == 'groupchat':
                to = to.split('/', 1)[0]

        twistedStanza['from'] = self.jidString(self.username, inForum)
        twistedStanza['to'] = to
        if messageType:
            twistedStanza['type'] = messageType

        body = domish.Element((JABBER_CLIENT_NS, 'body'))
        body.addChild(message)
        twistedStanza.addChild(body)
        return twistedStanza

    def sendMessage(self, message, to, messageType):
        if not self.mute:
            msgStanza = self.assembleMessage(message, to, messageType)
            reactor.callFromThread(self.send, msgStanza)

    def requestRoster(self):
        if self._waitingRoster:
            return
        self._waitingRoster = True
        iq = domish.Element((JABBER_CLIENT_NS, 'iq'))
        iq['type'] = 'get'
        iq.addElement(('jabber:iq:roster', 'query'))
        self.send(iq)
        # reset the timer

    def checkAccess(self, fromJid, messageType):
        """Access control plugins"""
        if messageType == 'groupchat':
            # no access control for group chat.
            # need a way to tell exactly which user sent a message, but is it
            # posslbe?
            return fromJid
        elif messageType == 'presence':
            pass
            # do something with these
        authorized = False
        user = fromJid
        for plugin in getPluginsByCapability('accessControl', self):
            self.logger.debug('Calling access control plugin %s for %s' % (plugin, user))
            authorized = plugin.call(sender = user, xmppAdapter = self, 
                                    log = self.pluginLogger)
            self.logger.debug('The user %s authorization result is %s' % (fromJid, authorized))
            # return the first positive response
            if authorized:
                return fromJid
        self.logger.debug('Done looking for access control plugin.')
        self.logger.debug('The user %s authorization result is %s' % (fromJid, authorized))
        return False

    def checkInvite(self, twistedStanza):
        """Check a message for a room invite.  Honor the request if it does"""
        for element in twistedStanza.elements():
            if element.uri == 'jabber:x:conference':
                room = element['jid'].split('@', 1)[0]
                self.logger.debug('Processing invitation to %s' % room)
                self.joinChatrooms(room)
                break

    def fromRoom(self, sender):
        return re.search(self.groupServer, sender)

    def getMUCJID(self, twistedStanza):
        sender = None
        # Get the actual sender JID if in muc or 121 muc
        for element in twistedStanza.elements():
            self.logger.debug('Looking at element %s' % element.toXml())
            if element.uri == 'http://jabber.org/protocol/nick':
                sender = element.children[0]
                break
        if sender is None:
            self.logger.debug('Could not find the MUC nick for jabber message %s' % twistedStanza.toXml())
            sender = twistedStanza['from'].partition('/')[0]
        return sender.encode('ascii', 'ignore')

    def getListOfTokens(self, s):
        self.logger.debug('Tokenizing string: %s' % s)
        # ensure the string is ascii chars only, or tokenizing will fail
        s = s.encode('ascii', 'ignore')
        tokenize = StringIO.StringIO(s)
        return csv.reader(tokenize, delimiter=' ').next()

    def send(self, twistedStanza):
        """send a twisted stanza element"""
        self.logger.debug('-> sending %s' % twistedStanza.toXml())
        self._send(twistedStanza)
