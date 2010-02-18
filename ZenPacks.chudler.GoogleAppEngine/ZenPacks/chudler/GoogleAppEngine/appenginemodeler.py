"""Inspired by the Zenoss Enterprise VMware ESX Plugin"""
import time

import Globals
from Products.ZenEvents import Event
from Products.ZenHub.PBDaemon import PBDaemon
from Products.ZenUtils.Driver import drive, driveLater
from ZenPacks.chudler.GoogleAppEngine.gaeclient import createGAEClient
from ZenPacks.chudler.GoogleAppEngine.AppEngineObjectProperties import ApplicationProperties, AppEngineInstance
from ZenPacks.chudler.GoogleAppEngine.AppEngineInstanceConfiguration import AppEngineInstanceConfiguration

class appenginemodeler(PBDaemon):

    singleInstance=None
    initialServices = PBDaemon.initialServices + ['ZenPacks.chudler.GoogleAppEngine.services.AppEngineConfigService']

    name = 'appenginemodeler'

    def __init__(self):
        PBDaemon.__init__(self)
        self.instanceInventory = []
        self.modelRunning = False

    def buildOptions(self):
        """
        stores the command-line/config file options
        """
        PBDaemon.buildOptions(self)
        self.parser.add_option('-a', '--app',
            dest='singleInstance',
            default=None,
            help="single GAE App to collect from")
        self.parser.add_option('--debug',
            dest='debug',
            default=False,
            action='store_true',
            help="turn on additional debugging")
        self.parser.add_option('--configCycleInterval',
            dest='configCycleInterval',
            default=60 * 4,  # EVERY 4 HOURS
            type='int',
            help="Period between modeling in minutes")
        self.parser.add_option('--showHttp',
            dest='showHttp',
            action='store_true',
            help="Show all http interactions")


    def service(self):
        """
        Retrieve the config service using getServiceNow so that
        it's not stale

        @return: the hub service that returns instance information
        @rtype: L{services.AppEngineConfigService}
        """
        return self.getServiceNow(self.initialServices[-1])

    def connected(self):
        """
        Called after daemon-hub connection is set up. This method
        kicks off the collection cycle.
        """

        def inner(driver):
            try:
                now = time.time()
                yield self.service().callRemote('getThresholdClasses')
                self.remote_updateThresholdClasses(driver.next())

                yield self.service().callRemote('getDefaultRRDCreateCommand')
                createCommand = driver.next()

                yield self.service().callRemote('getCollectorThresholds')
                self.rrdStats.config(self.options.monitor,
                                     self.name,
                                     driver.next(),
                                     createCommand)


                if self.options.singleInstance:
                    self.log.info('connected():retrieving for single instance %s',
                                  self.options.singleInstance)
                    yield self.service().callRemote('getAppEngineInstanceConfiguration',
                                                    self.options.singleInstance)
                    instanceConfig = driver.next()
                    self.instanceInventory=[instanceConfig]
                else:
                    self.log.info('connected():retrieving all instances')
                    yield self.service().callRemote('getAllAppEngineInstanceConfigurations')
                    instanceConfigs = driver.next()
                    self.instanceInventory=instanceConfigs

                infrastructureMap = self.discoverInfrastructures()
                self.log.debug('connected():adding infrastructure remotely')
                for instance, infrastructure in infrastructureMap.iteritems():
                    if instance and infrastructure:
                        self.log.debug('instance class %s', instance.__class__)
                        self.log.debug('infrastructure %s', infrastructure)
                        yield self.service().callRemote('addInfrastructure',
                                                        instance,
                                                        infrastructure)
                        driver.next()
                        self.log.info('connected():finished added infrastructure')

                cycle = self.options.configCycleInterval * 60
                driveLater(cycle, inner).addCallbacks(success, err)
                self.sendEvents(
                    self.rrdStats.gauge('cycleTime', cycle, time.time() - now) +
                    self.rrdStats.gauge('endPoints', cycle, len(self.instanceInventory))
                    )
                self.heartbeatTimeout = cycle * 3
                self.log.debug('connected():FINISHED')
            except Exception, ex:
                self.log.debug('connected():Logging exception')
                self.log.exception(ex)
                raise ex

        def success(result):
            self.heartbeat()

        def err(result):
            self.log.error('Error in appenginemodeler: %s' % result)
            self.heartbeat()

        drive(inner).addCallbacks(success, err)

    def remote_updateEndpointConfiguration(self, instanceConfig):
        """
        Called by the hub to indicate that the appengine connection params have
        changed
        """
        self.log.info( 'Not updating instance configuration for %s'
                       % instanceConfig.id )

    def discoverInfrastructures(self):
        """
        Loop through the L{instanceInventory}, calling discoverInfrastructure on
        each

        @return: the infrastructures discovered at the instances
        @rtype: a C{map} of instance id (C{string}) to
                L{AppEngineObjectProperties.AppEngineInfrastructure}
        """
        infrastructureMap={}
        for instance in self.instanceInventory:
            infrastructure=self.discoverInfrastructure(instance)
            infrastructureMap[instance.id]=infrastructure
        return infrastructureMap

    def discoverInfrastructure(self, instanceConfig):
        """
        Model all the AppEngine objects visible from the given Google account

        @param instanceConfig: the target to retrieve info from
        @type instanceConfig: L{AppEngineInstanceConfiguration}

        @return: The AppEngine objects visible
        @rtype: L{AppEngineObjectProperties.AppEngineInstance}

        """
        self.log.debug('connected():calling discoverInfrastructure with %s',
                      instanceConfig)
        client=self.getGAEClient( instanceConfig )
        self.log.debug( 'Logged into instance' )
        applicationProperties = client.getAllApplicationsWithDefaultProperties()
        self.log.debug( 'Retrieved %i applications from instance' % len( applicationProperties ) )
        self.log.debug( 'Application properties: %s' % [a.attributes for a in applicationProperties])
        #taskQueueProperties = client.getAllTaskQueuesWithDefaultProperties()
        #self.log.debug( 'Retrieved %i task queues from instance' % len( taskQueueProperties ) )
        #self.log.debug( 'Task Queue properties: %s' % [a.attributes for a in taskQueueProperties])

        instance = AppEngineInstance()
        instance.addApplications(applicationProperties)
        #infrastructure.addTaskQueues(taskQueuProperties)
        return instance

    def getGAEClient(self, instance):
        """
        Create a client for retrieving AppEngine information

        @param instance: the target to connect to
        @type L{AppEngineInstanceConfiguration}
        """
        client = createGAEClient(instance.user,
                            instance.password, self.options.showHttp,
                            True, self.options.logseverity)
        return client


if __name__=='__main__':
    mymodeler = appenginemodeler()
    mymodeler.run()
