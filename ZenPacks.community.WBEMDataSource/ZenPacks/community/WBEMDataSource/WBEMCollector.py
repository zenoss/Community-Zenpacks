################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WBEMCollector

PB daemon-izable base class for creating WBEM collectors

$Id: WBEMPlugin.py,v 1.0 2009/08/04 23:08:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

import logging
import time

import Globals
from Products.ZenHub.PBDaemon import PBDaemon, FakeRemote
from Products.ZenEvents.ZenEventClasses import App_Start, Clear
from Products.ZenEvents.Event import Error
from Products.ZenUtils.Driver import drive, driveLater
from Products.ZenUtils.Utils import unused

# needed by pb
from Products.DataCollector import DeviceProxy
from Products.DataCollector.Plugins import PluginLoader
unused(DeviceProxy, PluginLoader)

from twisted.internet import reactor, defer
from twisted.python.failure import Failure


class WBEMCollector(PBDaemon):
    """
    Base class to be sub-classed by WBEM daemons
    """
    configCycleInterval = 20

    # Short text description of what this collector does: set in sub-classes
    whatIDo = 'Override whatIDo in a subclass'

    initialServices = PBDaemon.initialServices\
         + ['ZenPacks.community.WBEMDataSource.services.WbemPerfConfig']

    attributes = ('configCycleInterval', 'perfsnmpCycleInterval')
    deviceAttributes = (
        'manageIp', 'zWinPassword', 'zWinUser', 'zWbemPort', 'zWbemUseSSL')


    def __init__(self):
        self.devices = []
        PBDaemon.__init__(self)
        self.reconfigureTimeout = None

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
                self.log.info('Scanned %d devices in %.1f seconds',
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
        raise NotImplementedError('You must override this method.')

    def cycleInterval(self):
        """
        Return the length of time in a scan cycle

        Method which must be overridden
        
        @return: number of seconds in a cycle
        @rtype: int
        """
        raise NotImplementedError('You must override this method')


    def configService(self):
        """
        Gather this daemons WBEM configuration
        
        @return: zenhub configuration information
        @rtype: WbemPefConfig
        """
        return self.services.get('ZenPacks.community.WBEMDataSource.services.WbemPerfConfig')


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
        @type cfg: WBEMConfig
        """
        cfg = dict(cfg)
        for attribute in self.attributes:
            current = getattr(self, attribute, None)
            value = cfg.get(attribute)
            self.log.debug( "Received %s = %r from zenhub" % ( attribute, value))
            if current is not None and current != value:
                self.log.info('Setting %s to %r', attribute, value)
                setattr(self, attribute, value)
        self.heartbeatTimeout = self.cycleInterval() * 3

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

    def deviceDown(self, device, error):
        """
        Method to call when a device does not respond or returns an error. 
        
        @param device: device object
        @type device: device object
        @param error: useful and informative error message
        @type error: string
        """
        summary = \
            'Could not %s (%s). Check your username/password settings and verify network connectivity.'\
             % (self.whatIDo, error)
        self.sendEvent(dict(
            summary=summary,
            component=self.agent,
            eventClass='Status/WBEM',
            device=device.id,
            severity=Error,
            agent=self.agent,
            ))
        self.log.warning('Closing watcher of %s', device.id)

    def deviceUp(self, device):
        """
        Method to call when a device comes back to life.
        
        @param device: device oject
        @type device: device object
        """
        msg = 'WBEM connection to %s up.' % device.id
        self.sendEvent(dict(
            summary=msg,
            eventClass='Status/WBEM',
            device=device.id,
            severity=Clear,
            agent=self.agent,
            component=self.name,
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
