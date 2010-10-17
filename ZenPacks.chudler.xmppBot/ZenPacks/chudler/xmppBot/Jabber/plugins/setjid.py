"""Check if the sender is a valid zenoss admin.  For access control"""

from Jabber.Plugins import Plugin
from Jabber.ZenAdapter import ZenAdapter
from Jabber.Options import Options
from optparse import OptionError
import transaction

class SetJid(Plugin):

  name = 'mapuser'
  capabilities = ['setjid', 'mapuser', 'help']
  private = False

  def call(self, args, client, sender, messageType, log, **kw):
    log.debug('mapuser plugin running with %s' % args)
    opts = self.options()

    # parse the options
    try:
        (options, arguments) = opts.parse_args(args)
        log.debug('Done parsing arguments.  Options are "%s", arguments expanded to %s' % (options, arguments))
    except OptionError, message:
        client.sendMessage(message, sender, messageType)
        return False
    if options.zenUser is None or options.jabberId is None:
        client.sendMessage('No.  -u and -j are both required', sender, messageType)
        return False

    adapter = ZenAdapter()

    jabberId = options.jabberId.lower()

    haveUser = False
    for user in adapter.userSettings():
        if user.id.lower() == options.zenUser.lower():
            haveUser = True
            try:
                currentId = user.getProperty('JabberId')
            except AttributeError:
                currentId = False
            if currentId:
                if options.jabberId == currentId.lower():
                    if options.force:
                        self.mapIds(jabberId, user)
                        message = 'This user mapping already looks like this.  Forced option was used, so I set it anyway.'
                        client.sendMessage(message, sender, messageType)
                        return
                    else:
                        message = 'This user mapping already looks like this.'
                        client.sendMessage(message, sender, messageType)
                        return
                if '/' in sender:
                    sender = sender.split('/')[0]
                if currentId.lower() == sender.lower():
                    if options.force:
                        message = 'This is your Zenoss user id, and the mapping is already set correctly.  Changing it will prevent you from communicating with me.  If you really want to change it, do so from the Zenoss interface or -f.'
                        client.sendMessage(message, sender, messageType)
                        return
                    else:
                        self.mapIds(jabberId, user)
                        message = 'This is your Zenoss user id, and the mapping is already set correctly.  However, the force option was used, so I set it anyway.  Since this will probably break communication with me, you can change it back from the Zope interface.'
                        client.sendMessage(message, sender, messageType)
                        return
            log.debug('Setting the jabberid mapping property to %s for zenuser %s' % (jabberId, user))
            self.mapIds(jabberId, user)
            break

    if haveUser:
        message = 'JabberId for this user has been saved.  Thanks.'
        client.sendMessage(message, sender, messageType)
        return
    else:
        message = 'Sorry! I Could not find a Zenoss user by the name %s' % options.zenUser
        client.sendMessage(message, sender, messageType)
        return

  def mapIds(self, jabberId, zenUser):
    self.setPropertyIfNeeded(zenUser)
    zenUser._updateProperty('JabberId', jabberId)
    transaction.commit()

  def setPropertyIfNeeded(self, zenUser):
    if not zenUser.hasProperty('JabberId'):
        zenUser.manage_addProperty('JabberId', '', 'string')
        zenUser._setProperty('JabberId', '', 'string')
    try:
        zenUser.getProperty('JabberId')
    except AttributeError:
        zenUser.manage_addProperty('JabberId', '', 'string')

  def options(self):
    parser = Options(description = 'Acknowledge events by eventid', prog = 'ack')
    parser.add_option('-u', '--user', dest='zenUser', help='Zenoss username (must already exist in zenoss).')
    parser.add_option('-j', '--jid', dest='jabberId', help='JabberID to map to the zenoss user.')
    parser.add_option('-f', '--force', dest='force', action='store_true', help='Force association even if it could disallow your own user.  USE WITH CAUTION.')
    return parser

  def help(self):
    opts = self.options()
    return str(opts.help())
