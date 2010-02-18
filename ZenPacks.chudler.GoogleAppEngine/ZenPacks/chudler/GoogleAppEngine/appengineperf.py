"""Inspired by the Zenoss Enterprise VMware ESX Plugin"""

# TODO 3FEB10:  Need to code audit since many methods are not used, or used improperly
# This seems too complex for a simple task?

import os
import time
import Globals
import socket

from twisted.internet.defer import Deferred
from twisted.python import failure
from twisted.internet import defer, reactor
from twisted.spread import pb

from Products.ZenEvents import Event
from Products.ZenModel.RRDDataPoint import SEPARATOR
from Products.ZenRRD.RRDDaemon import RRDDaemon
from Products.ZenRRD.RRDUtil import RRDUtil
from Products.ZenRRD.Thresholds import Thresholds
from Products.ZenUtils.NJobs import NJobs
from Products.ZenUtils.Driver import drive, driveLater
from ZenPacks.chudler.GoogleAppEngine.gaeclient import createGAEClient
from ZenPacks.chudler.GoogleAppEngine.AppEngineInstanceConfiguration import AppEngineInstanceConfiguration
from ZenPacks.chudler.GoogleAppEngine.services.AppEnginePerfConfigService import RRDConfig, AppEngineDataSourceConfig


DEFAULT_HEARTBEAT_TIME = 5*60

class AppEnginePerf(RRDDaemon):
    initialServices = RRDDaemon.initialServices + [
        'ZenPacks.chudler.GoogleAppEngine.services.AppEnginePerfConfigService'
        ]

    #Hold on to datasources as a map of instances to applications to datasources
    datasourceMap={}

    def __init__(self):
        RRDDaemon.__init__(self, 'appengineperf')
        #map of deviceId -> deviceConfig
        self.deviceConfigs = {}
        self.running = False


    def connected(self):
        def configTask(driver):
            self.log.debug("configTask(): fetching config")
            yield self.fetchConfig()
            driver.next()
            driveLater(self.configCycleInterval*60, configTask)

        d = drive(configTask)

        d.addCallbacks(self.runCollection, self.errorStop)

    def remote_updateDeviceConfig( self, configMap ):
        self.log.debug( "ASYNC instance configuration update" )
        for instance, configs in configMap.iteritems():
            self.updateConfig( instance, configs )

    def updateConfig(self, instance, datasourceConfigs):
        """
        update device configurations to be collected
        """
        self.log.debug("updateConfig(): updating config for instance %s" %
                       instance)
        self.log.debug("updateConfig(): adding %i configs to monitor" %
                       len( datasourceConfigs ) )

        applicationsMap = {}
        for datasourceConfig in datasourceConfigs:
            if datasourceConfig.id in applicationsMap:
                applicationsMap[datasourceConfig.id].append(datasourceConfig)
            else:
                applicationsMap[datasourceConfig.id] = []

            self.log.debug("updateConfig(): datasource %s on %s: %s" % (datasourceConfig.datasourceId, datasourceConfig.id, datasourceConfig.rrdPath))
            self.thresholds.updateList(datasourceConfig.thresholds)

        self.datasourceMap.update({ instance : applicationsMap })


    def fetchConfig(self):
        """
        Get configuration values from ZenHub
        """
        def inner(driver):
            self.log.debug("fetchConfig(): Fetching config from zenhub")
            yield self.model().callRemote('getDefaultRRDCreateCommand')
            createCommand = driver.next()

            yield self.model().callRemote('propertyItems')
            self.setPropertyItems(driver.next())
            self.rrd = RRDUtil(createCommand, DEFAULT_HEARTBEAT_TIME)

            yield self.model().callRemote('getThresholdClasses')
            self.remote_updateThresholdClasses(driver.next())

            yield self.model().callRemote('getCollectorThresholds')
            self.rrdStats.config(self.options.monitor,
                                  self.name,
                                  driver.next(),
                                  createCommand)

            devices=self.getDevices()
            instances=self.getInstances()
            yield self.model().callRemote('getDeviceConfigs', instances, devices )
            configs = driver.next()
            self.log.debug('Fetched %i configs' % len( configs ) )
            if len(configs) == 0:
                self.log.info("fetchConfig(): No configs returned from zenhub")
            else:
                for instance in configs.keys():
                    deviceConfigs=configs[instance]
                    self.updateConfig(instance, deviceConfigs)
            self.log.debug("fetchConfig(): Done fetching config from zenhub")
        return drive(inner)


    def getDevices(self):
        devices=[]
        if self.options.device:
            devices = [self.options.device]
        return devices


    def getInstances(self):
        instances=[]
        if self.options.instance:
            instances = [self.options.instance]
        return instances


    def storeRRD(self, dsConfig, dpValue):
        """
        store a value into an RRD file
        """
        rrdConf = dsConfig.rrdConfig.values()[0]
        dpPath = dsConfig.rrdPath

        value = self.rrd.save(dpPath,
                              dpValue,
                              rrdConf.rrdType,
                              rrdConf.command)

        for ev in self.thresholds.check(dpPath, time.time(), value):
            eventKey = dsConfig.eventKey
            if ev.has_key('eventKey'):
                ev['eventKey'] = '%s|%s' % (eventKey, ev['eventKey'])
            else:
                ev['eventKey'] = eventKey
            self.sendThresholdEvent(**ev)


    def collectAppEngine(self, instance):

        def remoteCall(driver):
            ref_map = {}
            reverse_map = {}
            for application, dsConfigs in self.datasourceMap[instance].iteritems():
                for dsConfig in dsConfigs:
                    reverse_map[(dsConfig.metricId.counterId, instance,\
                                    application)] = dsConfig
            try:
                # TODO 2FEB10:  Need way to retrieve only a certain application
                metrics = gaeClient.retrieveDataPoints()
                processMetrics(metrics, reverse_map)
            except Exception, ex:
                self.log.warning( 'Error trying to retrieve' +
                                  ' and save metrics: %s' %
                                  [str(value) for value
                                   in ref_map.values() ] )
                self.log.exception(ex)

            yield defer.succeed("Collected %s datapoints" % instance.id)
            driver.next()

        def processMetrics(metrics, cfgmap):
            self.log.info('cfgmap:%s' % (cfgmap))
            for app_id, data in metrics.iteritems():
                for counterId, datapoint in data.iteritems():
                    #self.log.info('CounterId:%s, datapoint:%s, app_id:%s' % (counterId, data, app_id))
                    cfgKey = (counterId, instance, app_id)
                    # ignore metrics sent that we didn't ask for
                    if not cfgmap.has_key(cfgKey):
                        #self.log.info('REJECTING counterid:%s datapoint:%s.\ Instance is:%s  Application is:%s' % (counterId, datapoint, instance, app_id))
                        continue
                    self.log.info('Accepting counterid:%s datapoint:%s.\
 Instance is:%s  Application is:%s' %
                                  (counterId, datapoint, instance, app_id))
                    dsConfig = cfgmap[cfgKey]
                    self.storeRRD(dsConfig, datapoint)

        gaeClient = self.getGAEClient(instance)

        return drive(remoteCall)

    def getGAEClient(self, instance):
        client = createGAEClient(instance.user, instance.password,
                            self.options.showHttp, True,
                            self.options.logseverity )
        client.login()
        return client


    def runCollection(self, result = None):

        def doCollection(driver):
            self.log.debug("doCollection(): starting collection cycle")
            reactor.callLater(self.options.dataCollectInterval, self.runCollection)
            if not self.options.cycle:
                self.stop()
            if self.running:
                self.log.error("last appengine collection is still running")
                return
            self.running = True
            jobs = NJobs(200,
                         self.collectAppEngine,
                         self.datasourceMap.keys())
            yield jobs.start()
            driver.next()
            self.log.debug("doCollection(): exiting collection cycle")
            self.sendEvents(
            self.rrdStats.gauge('instances',
                                self.options.dataCollectInterval,
                                len(self.datasourceMap)) +
            self.rrdStats.counter('dataPoints',
                                  self.options.dataCollectInterval,
                                  self.rrd.dataPoints) +
            self.rrdStats.gauge('cyclePoints',
                                self.options.dataCollectInterval,
                                self.rrd.endCycle())
            )

        def handleFinish(results):
            self.running = False
            for result in results:
                if isinstance(result,failure.Failure):
                    self.log.error("handleFinish():Failure: %s"
                                   % result)
                    result.printDetailedTraceback()
                elif isinstance(result , Exception):
                    self.log.error("handleFinish():Exception: %s"
                                   % result)
                else:
                    self.log.debug("handleFinish(): success %s"
                                  % result)

        def handleError(error):
            self.running = False
            self.log.error("handleError():Error running doCollection: %s"
                           % error.printTraceback())


        d = drive(doCollection)
        d.addCallback(handleFinish)
        d.addErrback(handleError)
        return d


    def buildOptions(self):
        RRDDaemon.buildOptions(self)
        self.parser.add_option('-e', '--instance',
                               dest='instance',
                               default='',
                               type='string',
                               help="Single instance to collect data from")
        self.parser.add_option('--showHttp',
                               dest='showHttp',
                               default=False,
                               action='store_true',
                               help="If present, show all http interactions")
        self.parser.add_option('--callChunkSize',
                               dest='callChunkSize',
                               default=200,
                               type='int',
                               help="Number of performance requests to submit at once")
        self.parser.add_option('--dataCollectInterval',
                               dest='dataCollectInterval',
                               default=5*60, #5 minutes
                               type='int',
                               help="Number of seconds between data collection attempts")



    def stop(self):
        RRDDaemon.stop(self)


    def remote_deleteDevice(self, device):
        pass



if __name__ == '__main__':
    perf = AppEnginePerf()
    perf.run()
