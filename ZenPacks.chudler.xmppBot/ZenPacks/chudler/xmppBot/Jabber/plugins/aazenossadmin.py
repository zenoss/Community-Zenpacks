"""Check if the sender is a valid zenoss admin.  This is called on every
incomming message."""

from Jabber.Plugins import Plugin
from Jabber.ZenAdapter import ZenAdapter

class AAZenossAdminPlugin(Plugin):

  capabilities = ['accessControl']

  def call(self, sender, log, **kw):
    log.debug('Zenoss Admin user plugin running with %s' % sender)

    sender = sender.lower()

    # remove the resource from the sender
    if '/' in sender:
        sender = sender.split('/')[0]

    adapter = ZenAdapter()

    log.debug('Got a message from %s.  Going to look for a Zenoss user to map it to.' % sender)
    # look through all zenoss users until we find one with the sender's JabberID
    for user in adapter.userSettings():
        jabberProperty = user.getProperty('JabberId').lower()
        if jabberProperty == sender:
            log.debug('JabberID %s maps to the sender: %s.  This user is authorized.' % (jabberProperty, sender))
            return True

    log.debug('Unable to find a Zenoss user with jabberId!  This sender is NOT authorized: %s' % sender)
    return False

  def private(self):
    True
