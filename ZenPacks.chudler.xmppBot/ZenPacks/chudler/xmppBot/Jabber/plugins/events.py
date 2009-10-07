"""Show events from Zenoss.  Needs work!"""

from Jabber.Plugins import Plugin
from Jabber.ZenAdapter import ZenAdapter
from Jabber.Options import Options
from optparse import OptionError

class Events(Plugin):

  name = 'events'
  capabilities = ['events', 'issues', 'help']

  def call(self, args, log, **kw):
    log.debug('Event plugin running with %s' % args)

    opts = self.options()
    # parse the options
    try:
        (options, arguments) = opts.parse_args(args)
        log.debug('Done parsing arguments.  Options are "%s", arguments expanded to %s' % (options, arguments))
    except OptionError, message:
        return str(message)

    adapter = ZenAdapter()

    if options.acked:
        log.debug('Looking for Acknowledged events')
        message = 'Acknowledged Events\n'
        events = adapter.acknowledgedEvents()
    else:
        message = 'Current Events\n'
        events = adapter.newEvents()
    if options.device:
        devices = adapter.devices(options.device)
        if len(devices) == 0:
            return 'Cannot find a device, ip or mac named "%s"' % options.device
        deviceIds = [device.id for device in devices]
        print 'Found %d devices machting %s' % (len(devices), devices)
        events = filter(lambda event: event.device in deviceIds, events)

    if len(events) == 0:
        return 'Congratulations.  No events!'
    for event in events:
        if event.component:
            message += '%s %s (%s): (id:%s)\n' % (event.device, event.component, event.summary, event.evid)
        else:
            message += '%s: %s (id:%s)\n' % (event.device, event.summary, event.evid)
    return message

  def private(self):
    False

  def options(self):
    parser = Options(description = 'Acknowledge events by eventid', prog = 'ack')
    parser.add_option('-a', '--acked', dest='acked', action='store_true', help='Show acknowledged events only.  The default is to show "new" events')
    parser.add_option('-d', '--device', dest='device', help='Optional device to show events for.  Default is to show events for all devices.')
    parser.add_option('-s', '--severity', dest='severity', help='Minimum severity to display.  NOT IMPLEMENTED.')
    parser.add_option('-v', '--verbose', dest='severity', action='store_true', help='Show more details about the events.  NOISY.')
    return parser

  def help(self):
    opts = self.options()
    return str(opts.help())
