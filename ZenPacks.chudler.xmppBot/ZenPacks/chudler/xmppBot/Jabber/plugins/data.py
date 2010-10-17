"""Extract data from Zenoss RRD files."""

from Jabber.Plugins import Plugin
from Jabber.ZenAdapter import ZenAdapter
from Jabber.Options import Options
from optparse import OptionError

class Data(Plugin):

  name = 'data'
  capabilities = ['data', 'info', 'help']
  private = False

  def call(self, args, log, client, sender, messageType, **kw):

    log.debug('Data extraction plugin running with arguments %s' % args)

    opts = self.options()

    adapter = ZenAdapter()
    try:
        (options, arguments) = opts.parse_args(args)
        log.debug('Done parsing arguments.  Options are "%s", arguments expanded to %s' % (options, arguments))
    except OptionError, message:
        client.sendMessage(str(message), sender, messageType)
        return False

    if options.deviceName is None or (not options.list and options.dataPointName is None):
        message = 'NO.  You must specify both device and datapoint with -d and -p.'
        client.sendMessage(message, sender, messageType)
        return False

    devices = adapter.devices(options.deviceName)
    if len(devices) == 0:
        message = 'Cannot find a device, ip or mac for "%s"' % options.deviceName
        client.sendMessage(message, sender, messageType)
        return False

    log.debug('Found %d devices matching %s' % (len(devices), devices))

    if options.list:
        dataPoints = {}
        if options.subComponent:
            for device in devices:
                componentList = self.findComponent(device, options.subComponent)
                if componentList:
                    for component in componentList:
                        for validPoint in component.getRRDDataPoints():
                            dataPoints[validPoint.id] = '_'.join([ pathTuple[1] for pathTuple in validPoint.breadCrumbs()])
        else:
            for device in devices:
                for validPoint in device.getRRDDataPoints():
                    dataPoints[validPoint.id] = '_'.join([ pathTuple[1] for pathTuple in validPoint.breadCrumbs()])

        client.sendMessage('Valid datapoints:', sender, messageType)

        for name, path in dataPoints.iteritems():
            message = '%s (%s)\n' % (name, path)
            client.sendMessage(message, sender, messageType)

        return True

    log.debug('Going to look for datapoint %s' % options.dataPointName)
    # rrdtool cannot accept arguments in unicode, so convert dataPointName to ascii first
    self.obtainValues(client, sender, messageType, devices, options.dataPointName.encode('ascii', 'ignore'), options.subComponent, log)

  def subDevices(self, device):
    return device.getSubObjects()

  def obtainValues(self, client, sender, messageType, devices, dataPoint, component, log):
    log.debug('Have %d devices to check for %s' % (len(devices), dataPoint))

    for device in devices:
        log.debug('Checking %s. For the dataPoint %s' % (device.id, dataPoint))

        # try to get it directly from the device first.
        if self.hasDataPoint(device, dataPoint):
            log.debug('The device %s does have the dataPoint %s' % (device, dataPoint))
            value = device.getRRDValue(dataPoint)
            message = '%s: %s\n' % (device.id, value)
            client.sendMessage(message, sender, messageType)

        elif component is not None:

            if self.findComponent(device, component) is None:
                message = 'Sorry.  Cannot find a component %s on %s' % (component, device)
                client.sendMessage(message, sender, messageType)
                return False

            if self.hasDataPoint(component, dataPoint):
                value = component.getRRDValue(dataPoint)
                message = '%s %s: %s\n' % (device.id, component.id, value)
                client.sendMessage(message, sender, messageType)

            else:
                message = '%s %s: Does not have a datapoint named %s.  Remember, spelling and case matter.  Try -l for a list of datapoint' % (device.id, component.id, dataPoint)
                client.sendMessage(message, sender, messageType)
        else:
            message = '%s: Unable to find the datapoint %s. Remember, spelling and case matter.  Try -l for a list of datapoints' % (device.id, dataPoint)
            client.sendMessage(message, sender, messageType)

  def hasDataPoint(self, entity, dataPoint):
    hasPoint = False
    for point in entity.getRRDDataPoints():
        if point.__name__ == dataPoint:
            hasPoint = True
            break
    return hasPoint

  def findComponent(self, device, components):
    componentList = []
    try:
        componentList = getattr(device.hw, components.split('.')).pop()()
    except AttributeError:
        try:
            componentList = getattr(device.os, components.split('.')).pop()()
        except AttributeError:
            """the user can specifiy dot-seperated components N level deep with -s os.someCard.somePort.interfaces.
            In practice, device associations are rarely more than one level deep.  In any case, we
            will take the last part of the association to be the actual component, and everything
            between to be an association.  So in this example os, someCard, somdPort would be walked, and
            interfaces() would be called to extract the value requested.  User's are likely to make an error,
            but I don't have a better way to do it right now.
            """
            component = self.walkComponents(device, components.split('.')[:-1])
            if component is not None:
                # try to call the method by name from the end of the users's subcomponent
                try:
                   componentList = getattr(component, components.split('.').pop())()
                except AttributeError:
                    return None
    return componentList

  def walkComponents(self, entity, remainder):
    """This is a recursive function that will walk down each subcomponent and return the last one"""
    for sub in remainder:
        try:
            newSub = getattr(entity, sub)
            # recurse to the next component, if there is one
            self.walkComponents(newSub, remainder[1:])
        except AttributeError:
            return None
    return entity

    # parse the options
  def options(self):
    parser = Options(description = 'Retrieve latest value read from the device for datapoint.  Simple example:\n data -d 10.1.1.1 -p laLoadInt1', prog = 'data')
    parser.add_option('-d', '--device', dest='deviceName', help='Device name, IP or MAC.')
    parser.add_option('-p', '--point', dest='dataPointName', help='Acknowledge all events.  If -e is also specified, it will still acknowledge every event.')
    parser.add_option('-l', '--list', dest='list', action='store_true', help='Only list datapoints for the device and/or component.')
    parser.add_option('-s', '--subcomponent', dest='subComponent', help='Optional subcomponent name, if the datapoint does not reside directly on the device.  You will probably have to specify this.  Here are two usage example:\n  data -d buffalo.example.com -p usedBlocks -s filesystems\n data -10.1.1.1 -p ifInErrors -s interfaces')
    return parser

  def help(self):
    opts = self.options()
    return str(opts.help())
