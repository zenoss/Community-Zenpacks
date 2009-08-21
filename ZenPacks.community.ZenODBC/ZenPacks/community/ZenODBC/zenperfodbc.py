################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OdbcCollector

PB daemon-izable base class for creating Odbc collectors

$Id: OdbcPlugin.py,v 1.0 2009/08/14 23:43:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

import logging
import time

import Globals
from Products.ZenHub.PBDaemon import PBDaemon, FakeRemote
from Products.ZenEvents.ZenEventClasses import App_Start, Clear
from Products.ZenEvents.Event import Error
from Products.ZenUtils.Driver import drive, driveLater
from Products.ZenUtils.Utils import unused
from OdbcClient import OdbcClient, CError

# needed by pb
from Products.DataCollector import DeviceProxy
from Products.DataCollector.Plugins import PluginLoader
unused(DeviceProxy, PluginLoader)

from twisted.internet import reactor, defer
from twisted.python.failure import Failure
from Products.ZenUtils.Timeout import timeout
from Products.ZenRRD.RRDUtil import RRDUtil
from Products.ZenRRD.Thresholds import Thresholds


class zenperfodbc(PBDaemon):
    """
    Odbc daemon
    """
    name = agent = "zenperfodbc"

    configCycleInterval = 20

    whatIDo = 'read the data from ODBC source'

    initialServices = PBDaemon.initialServices\
         + ['ZenPacks.community.ZenODBC.services.OdbcPerfConfig']

    attributes = ('configCycleInterval', 'perfsnmpCycleInterval')
    deviceAttributes = ('manageIp',)


    perfsnmpCycleInterval = 300
    thresholds = None
    rrd = None


    def __init__(self):
        self.devices = []
        PBDaemon.__init__(self)
        self.reconfigureTimeout = None
        self.thresholds = Thresholds()

    def remote_notifyConfigChanged(self):
        """
        Called from zenhub to push new configs down. 
        """
        self.log.info('Async config notification')
        if self.reconfigureTimeout and \
             not self.reconfigureTimeout.called:
            self.reconfigureTimeout.cancel()
        self.reconfigureTimeout = reactor.callLater(
                self.cycleInterval() / 2, drive, self.reconfigure)

    def stopScan(self, unused=None):
        """
        Stop (reactor.stop()) the collection
        
        @param unused: unused
        @type unused: string
        """
        self.stop()

    def scanCycle(self, driver):
        """
        Generator function to collect data in one scan cycle
        
        @param driver: driver
        @type driver: string
        @return: defered task
        @rtype: Twisted defered or DeferredList
        """
        now = time.time()
        cycle = self.cycleInterval()
        try:
            devices = []
            if self.devices is not None:
                for device in self.devices:
                    if not device.plugins:
                        continue
                    if self.options.device and device.id\
                         != self.options.device:
                        continue
                    devices.append(device)
            yield self.processLoop(devices, cycle)
            driver.next()
            if not self.options.cycle:
                self.stopScan()
            else:
                self.heartbeat()
                count = len(self.devices)
                if self.options.device:
                    count = 1
                delay = time.time() - now
                self.sendEvents(self.rrdStats.gauge('cycleTime', cycle,
                                delay) + self.rrdStats.gauge('devices',
                                cycle, count))
                self.log.info('Processed %d devices in %.1f seconds',
                              count, delay)
        except (Failure, Exception), ex:
            self.log.exception('Error processing main loop')
        
        # Schedule the next scan even if there was an error this time.
        if self.options.cycle:
            delay = time.time() - now
            driveLater(max(0, cycle - delay), self.scanCycle)
            

    def processLoop(self, devices, timeoutSecs):
        """
        Cycle through the list of devices and collect from them. 
        
        @param devices: device object list
        @type devices: list
        @param timeoutSecs: timeoutSecs
        @type timeoutSecs: int
        @return: list of defereds to processDevice()
        @rtype: Twisted DeferredList
        """
        deferreds = []
        for device in devices:
            deferreds.append(self.processDevice(device, timeoutSecs))
        return defer.DeferredList(deferreds)

    def processDevice(self, device, timeoutSecs):
        """
        Perform a collection service on a device 
        
        @param device: device to query
        @type device: object
        @param timeoutSecs: timeoutSecs
        @type timeoutSecs: int
        @return: defered to complete the processing
        @rtype: Twisted defered
        """
        def cleanup(result=None):
            if isinstance(result, Failure):
                self.componentDown(device, result.getErrorMessage())
        def inner(driver):
            try:
                if not device.queries:
                    driver.finish(None)
                self.log.info("Processing %s", device.id)
                odbcc = OdbcClient(device)
                yield odbcc.query(device.queries)
                q = driver.next()
		for tableName, data in q.iteritems():
		    if isinstance(data[0], CError):
		        component = device.datapoints[tableName][0][1]
		        error = data[0].getErrorMessage()
		        self.componentDown(device, error, component=component)
		        continue
		    if not data:
		        component = device.datapoints[tableName][0][1]
		        self.componentDown(device, None, component=component)
		        continue
		    for dp in device.datapoints[tableName]:
		        value = data[0].get(dp[0], None)
		        if value:
		            self.storeRRD(dp, long(value))
		    self.componentUp(device, component=dp[1])
		self.componentUp(device, component=None)
                self.log.info("Finished processing %s", device.id)
            except Exception, ex:
                self.log.exception(ex)
                raise
            self.niceDoggie(self.cycleInterval())
        if not device.plugins:
            return defer.succeed(None)
        d = timeout(drive(inner), timeoutSecs)
        d.addErrback(cleanup)
        return d

    def storeRRD(self, dp, value):
        dpname, comp, rrdPath, rrdType, rrdCreateCommand, minmax = dp
        value = self.rrd.save(rrdPath,
                                value,
                                rrdType,
				rrdCreateCommand,
                                min=minmax[0],
                                max=minmax[1])
        self.log.debug("RRD save result: %s" % value)

        for ev in self.thresholds.check(rrdPath, time.time(), value):
            self.log.debug("Event: %s" % ev)
            ev['component'] = comp
            self.sendEvent(ev)


    def fetchDevices(self, driver):
        yield self.configService().callRemote('getDeviceListByMonitor',
                                              self.options.monitor)

        yield self.configService().callRemote('getDeviceConfigAndOdbcDatasources', 
                                              driver.next())

        self.updateDevices(driver.next())

        yield self.configService().callRemote('getDefaultRRDCreateCommand')
        createCommand = driver.next()

        self.rrd = RRDUtil(createCommand, self.perfsnmpCycleInterval)


    def cycleInterval(self):
        """
        Return the length of time in a scan cycle

        Method which must be overridden
        
        @return: number of seconds in a cycle
        @rtype: int
        """
        return self.perfsnmpCycleInterval


    def configService(self):
        """
        Gather this daemons Odbc configuration
        
        @return: zenhub configuration information
        @rtype: OdbcPefConfig
        """
        return self.services.get('ZenPacks.community.ZenODBC.services.OdbcPerfConfig')


    def devicesEqual(self, d1, d2):
        for att in self.deviceAttributes:
            if getattr(d1, att, None) != getattr(d2, att, None):
                return False
        return True


    def updateDevices(self, devices):
        """
        Update device configuration
        
        @param devices: list of devices
        @type devices: list
        """
        self.devices = devices
	for c in devices:
            self.thresholds.updateForDevice(c.id, c.thresholds)


    def remote_deleteDevice(self, deviceId):
        """
        Function called from zenhub to remove a device from our
        list of devices.
        
        @param deviceId: deviceId
        @type deviceId: string
        """
        devices = []
        for d in self.devices:
            if deviceId == d.id:
                self.log.info("Stopping monitoring of %s.", deviceId)
            else:
                devices.append(d)
        self.devices = devices


    def error(self, why):
        """
        Twisted errback routine to log messages
        
        @param why: error message
        @type why: string
        """
        self.log.error(why.getErrorMessage())


    def updateConfig(self, cfg):
        """
        updateConfig
        
        @param cfg: configuration from zenhub
        @type cfg: OdbcConfig
        """
        cfg = dict(cfg)
        for attribute in self.attributes:
            current = getattr(self, attribute, None)
            value = cfg.get(attribute)
            self.log.debug( "Received %s = %r from zenhub" % ( attribute, value))
            if current is not None and current != value:
                self.log.info('Setting %s to %r', attribute, value)
                setattr(self, attribute, value)
        self.heartbeatTimeout = self.perfsnmpCycleInterval * 3

    def start(self):
        """
        Startup routine
        """
        self.log.info('Starting %s', self.name)
        self.sendEvent(dict(summary='Starting %s' % self.name,
                       eventClass=App_Start,
                       device=self.options.monitor, severity=Clear,
                       component=self.name))

    def startScan(self, unused=None):
        """
        Calls start() and then goes through scanCycle() until finished
        
        @param unused: unused
        @type unused: string
        """
        self.start()
        d = drive(self.scanCycle)


    def componentDown(self, device, error, component=None):
        """
        Method to call when a component returns no data. 
        
        @param device: device object
        @type device: device object
        @param comp: component object
        @type comp: component object
        @param error: useful and informative error message
        @type error: string
        """
        if not component:
            component = self.agent
        if not error:
            summary = 'Database %s is Unavailable.'%component
        else:
            summary = \
            'Could not %s (%s). Check your username/password settings and verify network connectivity.'\
             % (self.whatIDo, error)
        self.sendEvent(dict(
            summary=summary,
            component=component,
            eventClass='/Status/Odbc',
            device=device.id,
            severity=Error,
            agent=self.agent,
            ))

    def componentUp(self, device, component=None):
        """
        Method to call when a component comes back to life.
        
        @param device: device oject
        @type device: device object
        @param comp: component object
        @type comp: component object
        """
        if not component:
            component = self.agent
            summary = 'Odbc connection to %s up.' % device.id
        else:
            summary = 'Database %s is Active.'%component
        self.sendEvent(dict(
            summary=summary,
            eventClass='/Status/Odbc',
            device=device.id,
            severity=Clear,
            agent=self.agent,
            component=component,
            ))


    def reconfigure(self, driver):
        """
        Gather our complete configuration information.
        
        @param driver: driver object
        @type driver: driver object
        @return: defered
        @rtype: Twisted defered
        """
        try:
            yield self.configService().callRemote('getConfig')
            self.updateConfig(driver.next())

            yield drive(self.fetchDevices)
            driver.next()

            yield self.configService().callRemote('getThresholdClasses')
            self.remote_updateThresholdClasses(driver.next())

            yield self.configService().callRemote('getCollectorThresholds'
                    )
            self.rrdStats.config(self.options.monitor, self.name,
                                 driver.next())
        except Exception, ex:
            self.log.exception('Error fetching config')

    def startConfigCycle(self):
        """
        Gather configuration and set up to re-check.
        
        @return: defered
        @rtype: Twisted defered
        """
        def driveAgain(result):
            """
            callback and errback to gather configurations 
            
            @param result: result
            @type result: value
            @return: defered
            @rtype: Twisted deferrd
            """
            driveLater(self.configCycleInterval * 60, self.reconfigure)
            return result

        return drive(self.reconfigure).addBoth(driveAgain)

    def connected(self):
        """
        Method called after a connection to zenhub is established.
        Calls startConfigCycle() and startScan()
        """
        d = self.startConfigCycle()
        d.addCallback(self.startScan)

    def buildOptions(self):
        """
        Command-line option builder
        """
        PBDaemon.buildOptions(self)
        self.parser.add_option('-d', '--device', dest='device',
                               default=None,
                               help='The name of a single device to collect')
        self.parser.add_option('--debug', dest='debug', default=False,
                               action='store_true',
                               help='Increase logging verbosity.')

if __name__ == "__main__":
    from ZenPacks.community.ZenODBC.zenperfodbc import zenperfodbc
    zw = zenperfodbc()
    zw.run()
