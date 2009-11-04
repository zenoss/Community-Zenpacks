#!/usr/bin/python
"""jabber bot"""

"""This needs to be rewritten so that TwistedJabberClient and JabberAdapter are
One class.  They are very promiscuous as it is, and are lacking a real design."""

import re
import logging

log = logging.getLogger('zen.xmppBot')
log.setLevel(10)

from twisted.words.xish import xmlstream
from twisted.words.protocols.jabber import client, jid
from twisted.words.xish import domish
from twisted.internet import reactor, protocol

try:
    from twisted.internet import ssl
except ImportError:
    pass
    
from Plugins import getPluginsByCapability
from twisted.internet.task import LoopingCall

JABBER_CLIENT_NS = 'jabber:client'

   
class TwistedJabberClient:

    def __init__(self, dialogHandler, server, userId, userPassword, groupServer, realHost, wants_ssl, firstRoom, debug):
        self.dialogHandler = dialogHandler
        self.server = server
        try:
            self.host, self.port = server.split(':')
        except ValueError:
            self.host = server
            self.port = 5222
        else:
            self.port = int(self.port)
        self.userId = userId
        self.userPassword = userPassword
        self.wants_ssl = wants_ssl

        if realHost:
            self.realHost = realHost
        else:
            self.realHost = self.host

        if groupServer:
            if '.' in groupServer:
                self.groupServer = groupServer
            else:
                self.groupServer = '%s.%s' % (groupServer, realHost)
        else:
            self.groupServer = 'conference.%s' % realHost

        self.firstRoom = firstRoom
        self._fact = None
        self._send = None
        self.debug = debug
        self._waitingRoster = False
        self.connected = False

    def dprint(self, message):
      if self.debug:
        log.debug(message)
        
    def jidString(self, user, conf=False, resource=True):
        """make and return a Jabber identifier (jid) for a user's nick.

        if conf is a non empty string, use this string as the conference room
        and go through the conferences server

        if resource is true, append the 'bot' resource to the jid
        """
        if conf:
            if '@' not in conf:
              if resource:
                  return '%s@%s/%s' % (conf, self.groupServer, user)
              return '%s@%s' % (conf, self.groupServer)
        if '@' not in user:
          if resource:
              return '%s@%s/bot' % (user, self.realHost)
          return '%s@%s' % (user, self.realHost)
        return user
    
    def connect(self):
        """connect to the jabber server"""
        self.dprint('Starting to connect')
        self.dprint('Building context factory for jid %s' % self.jidString(self.userId))
        jidStr = self.jidString(self.userId)
        self._fact = factory = client.basicClientFactory(jid.JID(jidStr), self.userPassword)
        factory.addBootstrap('//event/stream/authd', self.authenticate)
        factory.addBootstrap(client.BasicAuthenticator.INVALID_USER_EVENT, self.invalidUser)
        factory.addBootstrap(client.BasicAuthenticator.AUTH_FAILED_EVENT, self.fatalError)
        factory.addBootstrap(client.BasicAuthenticator.REGISTER_FAILED_EVENT, self.fatalError)

        self.dprint('connecting to server %s using id %s...' % (self.server, self.userId))
        if self.wants_ssl:
            class contextFactory:
                isClient = 1
                method = ssl.SSL.SSLv3_METHOD

                def getContext(self):
                    context = ssl.SSL.Context(self.method)
                    return context

            self.dprint('Connecting with ssl...')
            ctxFactory = contextFactory()
            reactor.connectSSL(self.host, self.port, factory, ctxFactory)
        else:
            reactor.connectTCP(self.host, self.port, factory)
        return reactor

    def stop(self):
        """disconnect from the jabber server"""
        reactor.disconnectAll()
        self.connected = False
        reactor.stop()

    def send(self, twxml):
        """send a twisted xml element"""
        self.dprint('-> sending %s' % twxml.toXml())
        self._send(twxml)
        
    def authenticate(self, twxml):
        """authentication callback"""
        # bind twxml.send to self
        self._send = twxml.send
        # add observer for incoming message / presence requests
        twxml.addObserver('/iq',       self.iqHandler)
        twxml.addObserver('/presence', self.dialogHandler.presenceHandler)
        twxml.addObserver('/message',  self.dialogHandler.messageHandler)
        self.dprint('connected')
        self.requestRoster()
        keepalive = LoopingCall(self.loopEntry)
        keepalive.start(60)
        self.connected = True
        if self.firstRoom:
          # join a chatroom.
          self.dprint('First chatroom to join %s.  Joining...' % (self.firstRoom))
          forum = self.jidString(self.userId, self.firstRoom)
          self.send(presenceElement(self.jidString(self.userId), forum))
          self.dprint('Done sending presence to room %s' % (self.firstRoom))

    def loopEntry(self):
      self.sendPresence()

    def requestRoster(self):
      if self._waitingRoster:
        return
      self._waitingRoster = True
      iq = domish.Element((JABBER_CLIENT_NS, 'iq'))
      iq['type'] = 'get'
      iq.addElement(('jabber:iq:roster', 'query'))
      self.send(iq)
      # reset the timer

    def sendPresence(self):
      """Let client know we are still here"""
      presence = domish.Element((JABBER_CLIENT_NS, 'presence'))
      presence.addElement('status').addContent('Online')
      self.send(presence)

    def invalidUser(self, twxml):
        """invalid user callback"""
        self.fatalError(twxml)

    def fatalError(self, twxml):
        """unrecoverable error callback"""
        print 'unrecoverable error:'
        print twxml.toXml()
        self.stop()

    def iqHandler(self, twxml):
        """handle a iq packet
        TODO 09JUN09: test this.
        :type twxml: `twisted.xish.domish.Element`
        :param twxml: the xml stream containing a iq element
        """
        if self._waitingRoster and twxml.query.uri == 'jabber:iq:roster':
            # got roster, send presence so clients know we're actually online
            self.sendPresence()
            self._waitingRoster = False


class JabberAdapter:
    """actions for the jabber client"""

    def __init__(self, debug=True):
        self.debug = debug
        self.mute = False # mute chat command acts globally
        self.client = None # will be set later due to a cyclic dependency

    def dprint(self, message):
      if self.debug:
        log.debug(message.encode('ascii', 'ignore'))

    def checkAccess(self, twxml):
        """Access control plugins"""
        fromJid = twxml['from']
        messageType = twxml.attributes.get('type', 'nothing')
        if messageType == 'groupchat':
            # no access control for group chat.
            # need a way to tell exactly which user sent a message, but is it
            # posslbe?
            return fromJid
	elif messageType == 'presence':
	    pass
	    # do something with these
        elif messageType == 'nothing':
            for elmt in twxml.elements():
                for child in elmt.children:
                    try:
                        if child.name == 'invite':
                            fromJid = child['from']
                            log.debug('Invited to a room from %s.  Need to see if this user is authorized.' % fromJid)
                            break
                    except AttributeError:
                        pass
        authorized = False
        user = fromJid
        for plugin in getPluginsByCapability('accessControl'):
            self.dprint('Calling access control plugin %s for %s' % (plugin, user))
            authorized = plugin.call(sender = user, xmppAdapter = self, client = self.client, log = log)
        self.dprint('Done looking for access control plugin.')
        self.dprint('The user %s authorization result is %s' % (fromJid, authorized))
        if authorized:
          return fromJid
        else:
          return False

    def sendAction(self, action):
        """give xml object to the jabber client"""
        self.client.send(action)

    def presenceHandler(self, twxml):
        """jabber client hook: handle a presence packet, transform it
        into the right action and give it back

        :type twxml: `twisted.xish.domish.Element`
        :param twxml: the xml stream containing a presence element
        """
        self.dprint('-< received %s' % twxml.toXml())
        sender = self.checkAccess(twxml)
        if sender:
            messageType = twxml.attributes.get('type', 'nothing')
            if messageType == 'subscribe':
                self.sendAction(presenceElement(self.client.jidString(self.client.userId), twxml['from'], 'subscribed'))
        
    def messageHandler(self, twxml):
        """jabber client hook: handle a message packet, transform it
        into the right action and give it back to the dialog tester

        :type twxml: `twisted.xish.domish.Element`
        :param twxml: the xml stream containing a message element
        """
        # ignore delayed / error messages
        for elmt in twxml.elements():
          if elmt.uri == 'jabber:x:delay' or elmt.getAttribute('type') == 'error':
            self.dprint('*** dropped delayed msg %s' % twxml.toXml())
            return
        fromJid = twxml['from']
        self.dprint('-< received %s' % twxml.toXml())
        messageType = twxml.attributes.get('type', 'nothing')
        sender = self.checkAccess(twxml)
        if sender:
            for elmt in twxml.elements():
                # invited in a group chat ?
                if elmt.uri == 'jabber:x:conference':
                    room = elmt['jid'].split('@', 1)[0]
                    self.dprint('Processing invitation to %s' % room)
                    self.sendAction(self.acceptInvitation2twxml(room))
                    self.inForum = room
                    break
            try:
                quser, resource = fromJid.split('/', 1)
            except ValueError:
                self.dprint('*** dropping message from %s (no resource set)' % fromJid)
                return
            sender = fromJid.split('/', 1)[1]
            if sender == self.client.userId:
                self.dprint('*** dropping request from %s, is self' % fromJid)
                return
            sender = self.checkAccess(twxml)
            if sender:
              for elmt in twxml.elements():
                if elmt.name == 'body':
                  self.dprint('Processing chat body %s' % elmt.toXml())
                  body = elmt.children[0]
                  command = self.checkCommand(body, twxml['from'], messageType)
                  message = self.dispatchCommand(command, twxml['from'], body, twxml)
                  if message:
                    self.sendMessage(message, twxml['from'], messageType)
                  break

    def sendMessage(self, message, to, messageType):
      if not self.mute:
        msgStanza = self.sendMessage2twxml(message, to, messageType)
        self.sendAction(msgStanza)

    def checkCommand(self, message, fromJid, messageType):
        """Take the message and return a dict of its parts for command dispatching"""
        self.dprint('Checking message %s' % message)
        command = {}
        # TODO 19MAY09: switch to str.partition() when Zenoss gets to python 2.5
        commandPart = None
        to = None
        if '!.' in message:
          to, commandPart = message.split('!.')
        elif self.client.userId in message:
          to, commandPart = message.split('%s:' % self.client.userId)
        if commandPart is None:
          if not self.fromRoom(fromJid) or messageType == 'chat':
            commandPart = message
            to = self.client.userId
            self.dprint('Found command %s' % commandPart)
            command = {'parts':commandPart.strip().split(), 'to':to}
            return command
          else:
              return { 'parts':[message] }
        else:
          self.dprint('Someone addressed us with command %s' % commandPart)
          return {'parts':commandPart.strip().split(), 'to':'me'}

    def dispatchCommand(self, command, sender, originalMessage, twxml):
        """Find plugins that can respond to the command or execute all the plugins responding to default"""
        self.dprint('Dispatching command %s' % command)
        if command.has_key('to'):
          """Command is meant for the bot"""
          self.dprint('This is our command')
          plg = command['parts'].pop(0).lower()
          args = ''
          for arg in command['parts']:
            args += ' ' + arg.strip()
          message = ''
          """Handle a few high level commands: help, mute, unmute"""
          if plg == 'help':
            self.dprint('Finding plugins with help')
            message = 'In a groupchat, all commands start with "%s:" or "!."\nIn private chat, simply type the command.\nThese are the commands available.  For help on a command, try -h\n' % self.client.userId
            for plugin in getPluginsByCapability('help'):
              self.dprint('plugins %s has help' % plugin)
              message += plugin.name + '\n'
            return message
          elif plg == 'mute':
            self.mute = True
          elif plg == 'unmute':
            self.mute = False
            return 'At your service.'
          elif plg == 'default':
            # this is necessary to prevent users from invoking the catchall (default) plugins
            message = 'Unknown command.  Try help.'
          else:
            # find the plugins having the command name
            for plugin in getPluginsByCapability(plg):
              if not plugin.private():
                self.dprint('Calling plugin %s with %s' % (plg, args))
                message += plugin.call(args = args.strip().split(), xmppAdapter = self, client = self.client, message = originalMessage, sender = sender, twxml = twxml, log = log)
              else:
                self.dprint('Would have called plugins %s, but it is private' % plg)
            if not message:
              """Plugins that return no result
                 TODO:  give the plugin system tighter integration"""
              return 'Unknown command.  Try help.'
            return message
        else:
          # if the message is not a command, run every plugin with a default capability
          for plugin in getPluginsByCapability('default'):
            self.dprint('Calling default plugin %s sender:%s, room:%s, message:%s' % (plugin, sender, '', originalMessage))
            plugin.default(sender, '', originalMessage, self, self.client)
          return False

    def fromRoom(self, sender):
        return re.search(self.client.groupServer, sender)

    def sendMessage2twxml(self, message, sender, messageType):
        """transform a SendMessage action into a twisted xml element"""
        inForum = False
        resource = False
        twxml = domish.Element((JABBER_CLIENT_NS, 'message'))
        if self.fromRoom(sender) :
          inForum = sender.split('@', 1)[0]
          if messageType.lower() == 'groupchat':
            twxml['type'] = 'groupchat'
            self.dprint('We are in a forum and this message should go back to %s' % inForum)
          else:
            twxml['type'] = 'chat'
            resource = sender = sender.split('/')[-1]
        twxml['from'] = self.client.jidString(self.client.userId, inForum)
        twxml['to'] = self.client.jidString(sender, inForum, resource)
        body = domish.Element((JABBER_CLIENT_NS, 'body'))
        body.addChild(message)
        twxml.addChild(body)
        return twxml

    def acceptInvitation2twxml(self, room):
        """transform a SendPresence action into a twisted xml element"""
        forum = self.client.jidString(self.client.userId, room)
        """FIXME 09JUN09:  What userId goes in the next call?"""
        return presenceElement(self.client.jidString(self.client.userId), forum)

    def quitForum2twxml(self, action):
        """transform a SendPresence action into a twisted xml element"""
        """TODO 19JUNE09:  Test. Should work, but not called from anywhere yet."""
        forum = self.client.jidString(self.client.userId, action.content)
        return presenceElement(self.client.jidString(self.client.userId), forum, 'unavailable')


def presenceElement(from_, to, presenceType=None):
    """create and return a xml presence element"""
    twxml = domish.Element((JABBER_CLIENT_NS, 'presence'))
    twxml['from'] = from_
    twxml['to'] = to
    if presenceType:
        twxml['type'] = presenceType
    return twxml

class Plugin(object): 
    pass
