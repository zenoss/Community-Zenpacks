"""Model a device in Zenoss."""

from Jabber.Plugins import Plugin
from Jabber.ZenAdapter import ZenAdapter
from Jabber.Options import Options
from optparse import OptionError

class Model(Plugin):

  name = 'model'
  capabilities = ['model', 'create', 'help']

  def call(self, args, xmppAdapter, sender, twxml, log, **kw):
    log.debug('Modeler plugin running with arguments: %s' % args)
    
    adapter = ZenAdapter()
    opts = self.options()
    try:
        (options, arguments) = opts.parse_args(args)
        log.debug('Done parsing arguments.  Options are "%s", arguments expanded to %s' % (options, arguments))
    except OptionError, message:
        return str(message)
    if options.deviceName is None:
        return 'No.  -H or --host is required.'
    log.debug('Starting to load device.')
    xmppAdapter.sendMessage('Please wait while the device is loaded.', sender, twxml['type'])
    adapter.loadDevice(**options.__dict__)
    return 'Done discovering %s.' % options.deviceName

  def options(self):
    parser = Options(description = 'Create a new device to monitor', prog = 'model')
    parser.add_option('-H', '--host', dest='deviceName', help='Name of the host to model.')
    parser.add_option('-p', '--path', dest='devicePath', default='/Discovered', help='Place in Zenoss tree')
    parser.add_option('-t', '--tag', dest='tag', help='Tag Number')
    parser.add_option('-s', '--serial', dest='serialNumber', help='Serial number')
    parser.add_option('-c', '--snmp-secret', dest='zSnmpCommunity', default='public', help='SNMP Community string.  Configured in Zenoss')
    parser.add_option('-P', '--snmp-port', dest='zSnmpPort', default=161, help='SNMP Port to probe')
    parser.add_option('-v', '--snmp-version', dest='zSnmpVer', default='1', help='SNMP Version to use.  Configured in Zenoss')
    parser.add_option('-r', '--rack', dest='rackSlot', default=0, help='Rack slot.  Defaults to 0')
    parser.add_option('-n', '--state', dest='productionState', type='int', default=1000, help='Numerical production state.  Defaults to 1000 (production)')
    parser.add_option('-m', '--comment', dest='comments', help='Device comment.  No default')
    parser.add_option('-l', '--location', dest='locationPath', help='Zenoss tree location, NOT physical location.')
    parser.add_option('-d', '--protocol', dest='discoverProto', default='snmp', help='Discovery protocol.  Defaults to snmp.')
    return parser
    
  def private(self):
    return False

  def help(self):
    opts = self.options()
    return str(opts.help())
