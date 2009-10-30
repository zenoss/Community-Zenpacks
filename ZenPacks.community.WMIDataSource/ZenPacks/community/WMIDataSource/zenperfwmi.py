################################################################################
#
# This program is part of the WMIDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""zenperfwmi

Gets WMI performance data and stores it in RRD files.

$Id: zenperfwmi.py,v 2.1 2009/10/30 17:05:23 egor Exp $"""

__version__ = "$Revision: 2.1 $"[11:-2]

import logging

# IMPORTANT! The import of the pysamba.twisted.reactor module should come before
# any other libraries that might possibly use twisted. This will ensure that
# the proper WmiReactor is installed before anyone else grabs a reference to
# the wrong reactor.
import pysamba.twisted.reactor

import Globals
import zope.component
import zope.interface
import time

from twisted.internet import defer, reactor
from twisted.python.failure import Failure

from Products.ZenCollector.daemon import CollectorDaemon
from Products.ZenCollector.interfaces import ICollectorPreferences,\
                                             IDataService,\
                                             IEventService,\
                                             IScheduledTask
from Products.ZenCollector.tasks import SimpleTaskFactory,\
                                        SimpleTaskSplitter,\
                                        TaskStates
from Products.ZenEvents.ZenEventClasses import Error, Clear, Status_WinService
from Products.ZenUtils.observable import ObservableMixin
from Products.ZenWin.WMIClient import WMIClient
from Products.ZenWin.utils import addNTLMv2Option, setNTLMv2Auth

# We retrieve our configuration data remotely via a Twisted PerspectiveBroker
# connection. To do so, we need to import the class that will be used by the
# configuration service to send the data over, i.e. DeviceProxy.
from Products.ZenUtils.Utils import unused
from Products.ZenCollector.services.config import DeviceProxy
unused(DeviceProxy)

#
# creating a logging context for this module to use
#
log = logging.getLogger("zen.zenperfwmi")


#
# client class
#
class myWMIClient(WMIClient):
    def connect(self, namespace="root\\cimv2"):
        from pysamba.twisted.reactor import eventContext
        from pysamba.wbem.Query import Query
        import logging
        log = logging.getLogger("zen.WMIClient")
        log.debug("connect to %s, user %r", self.host, self.user)
        if not self.user:
            log.warning("Windows login name is unset: "
                        "please specify zWinUser and "
                        "zWinPassword zProperties before adding devices.")
            raise BadCredentials("Username is empty")
        self._wmi = Query()
        creds = '%s%%%s' % (self.user, self.passwd)
        return self._wmi.connect(eventContext, self.device.id, self.host,
                                creds, namespace)


# Create an implementation of the ICollectorPreferences interface so that the
# ZenCollector framework can configure itself from our preferences.
class ZenPerfWmiPreferences(object):
    zope.interface.implements(ICollectorPreferences)
    
    def __init__(self):
        """
        Construct a new ZenWinPreferences instance and provide default
        values for needed attributes.
        """
        self.collectorName = "zenperfwmi"
        self.defaultRRDCreateCommand = None
        self.cycleInterval = 5 * 60 # seconds
        self.configCycleInterval = 20 # minutes
        self.options = None
        
        # the configurationService attribute is the fully qualified class-name
        # of our configuration service that runs within ZenHub
        self.configurationService = 'ZenPacks.community.WMIDataSource.services.WmiPerfConfig'
        
        self.wmibatchSize = 10
        self.wmiqueryTimeout = 1000
        
    def buildOptions(self, parser):
        parser.add_option('--debug', dest='debug', default=False,
                               action='store_true',
                               help='Increase logging verbosity.')
        parser.add_option('--proxywmi', dest='proxywmi',
                               default=False, action='store_true',
                               help='Use a process proxy to avoid long-term blocking'
                               )
        parser.add_option('--queryTimeout', dest='queryTimeout',
                               default=None, type='int',
                               help='The number of milliseconds to wait for ' + \
                                    'WMI query to respond. Overrides the ' + \
                                    'server settings.')
        parser.add_option('--batchSize', dest='batchSize',
                               default=None, type='int',
                               help='Number of data objects to retrieve in a ' +
                                    'single WMI query.')
        addNTLMv2Option(parser)

    def postStartup(self):
        # turn on low-level pysamba debug logging if requested
        logseverity = self.options.logseverity
        if logseverity <= 5:
            pysamba.library.DEBUGLEVEL.value = 99

        # force NTLMv2 authentication if requested
        setNTLMv2Auth(self.options)


class ZenPerfWmiTask(ObservableMixin):
    zope.interface.implements(IScheduledTask)
        
    STATE_WMIC_CONNECT = 'WMIC_CONNECT'
    STATE_WMIC_QUERY = 'WMIC_QUERY'
    STATE_WMIC_PROCESS = 'WMIC_PROCESS'
    
    def __init__(self,
                 deviceId,
                 taskName,
                 scheduleIntervalSeconds,
                 taskConfig):
        """
        Construct a new task instance to get WMI data.
        
        @param deviceId: the Zenoss deviceId to watch
        @type deviceId: string
        @param taskName: the unique identifier for this task
        @type taskName: string
        @param scheduleIntervalSeconds: the interval at which this task will be
               collected
        @type scheduleIntervalSeconds: int
        @param taskConfig: the configuration for this task
        """
        super(ZenPerfWmiTask, self).__init__()
        
        self.name = taskName
        self.configId = deviceId
        self.interval = scheduleIntervalSeconds
        self.state = TaskStates.STATE_IDLE
        
        self._taskConfig = taskConfig
        self._devId = deviceId
        self._manageIp = self._taskConfig.manageIp
        self._namespaces = self._taskConfig.queries.keys()
        self._queries = self._taskConfig.queries
        self._thresholds = self._taskConfig.thresholds
        self._datapoints = self._taskConfig.datapoints
        
        self._dataService = zope.component.queryUtility(IDataService)
        self._eventService = zope.component.queryUtility(IEventService)
        self._preferences = zope.component.queryUtility(ICollectorPreferences,
                                                        "zenperfwmi")
                                                        
        self._wmic = {} # the WMIClient
        self._reset()
        
    def _reset(self):
        """
        Reset the WMI client and notification query watcher connection to the
        device, if they are presently active.
        """
	for namespace in self._namespaces:
            if namespace in self._wmic:
                self._wmic[namespace].close()
            self._wmic[namespace] = None
        self._wmic = {}
        
    def _finished(self, result):
        """
        Callback activated when the task is complete so that final statistics
        on the collection can be displayed.
        """

        self._reset()

        if not isinstance(result, Failure):
            log.debug("Device %s [%s] scanned successfully",
                      self._devId, self._manageIp)
        else:
            log.debug("Device %s [%s] scanned failed, %s",
                      self._devId, self._manageIp, result.getErrorMessage())

        # give the result to the rest of the callback/errchain so that the
        # ZenCollector framework can keep track of the success/failure rate
        return result

    def _failure(self, result, namespace=None):
        """
        Errback for an unsuccessful asynchronous connection or collection 
        request.
        """
        err = result.getErrorMessage()
        log.error("Unable to scan device %s: %s %s", self._devId, namespace, err)

        summary = """
            Could not get WMI Instance (%s). Check your
            username/password settings and verify network connectivity.
            """ % err

        self._eventService.sendEvent(dict(
            summary=summary,
            component='zenperfwmi',
            eventClass=Status_WinService,
            device=self._devId,
            severity=Error,
            agent='zenperfwmi',
            ))

        # give the result to the rest of the errback chain
        return result


    def _collectSuccessful(self, results):
        """
        Callback for a successful fetch of services from the remote device.
        """
        self.state = ZenPerfWmiTask.STATE_WMIC_PROCESS
        
        log.debug("Successful collection from %s [%s], results=%s",
                  self._devId, self._manageIp, results)
        
	if results:          
	    for tableName, data in results.iteritems():
		for (dpname, comp, rrdPath, rrdType, rrdCreate,
		                        minmax) in self._datapoints[tableName]:
		    if dpname == 'sysUpTime':
		        value = long(getattr(data[0], 'SystemUpTime',None)) * 100
		    else:
		        value = long(getattr(data[0], dpname, None))
                    self._dataService.writeRRD( rrdPath,
                                                value,
                                                rrdType,
			                        rrdCreate,
                                                min=minmax[0],
                                                max=minmax[1])
	return results

    def _collectCallback(self, result, namespace):
        """
        Callback called after a connect or previous collection so that another
        collection can take place.
        """
        log.debug("Polling for WMI data from %s [%s] %s", 
                  self._devId, self._manageIp, namespace)

        self.state = ZenPerfWmiTask.STATE_WMIC_QUERY
	d = self._wmic[namespace].query(self._queries[namespace])
        d.addCallbacks(self._collectSuccessful, self._failure)
        return d

    def _connectCallback(self, result):
        """
        Callback called after a successful connect to the remote Windows device.
        """
        log.debug("Connected to %s [%s]", self._devId, self._manageIp)
        

    def _connect(self, namespace):
        """
        Called when a connection needs to be created to the remote Windows
        device.
        """
        log.debug("Connecting to %s [%s] %s", self._devId, self._manageIp,
	                                                        namespace)
        self.state = ZenPerfWmiTask.STATE_WMIC_CONNECT
        self._wmic[namespace] = myWMIClient(self._taskConfig)
        d = self._wmic[namespace].connect(namespace=namespace)
        return d

    def cleanup(self):
        return self._reset()

    def doTask(self):
        log.debug("Scanning device %s [%s]", self._devId, self._manageIp)
        
        # connect to device
	pool = []
	for namespace in self._namespaces:
            pool.append(self._connect(namespace))
            pool[-1].addCallbacks(self._connectCallback, self._failure)

            # try collecting events after a successful connect, or if we're
            # already connected
            pool[-1].addCallback(self._collectCallback, namespace=namespace)
        dl = defer.DeferredList(pool, consumeErrors=True)

        # Add the _finished callback to be called in both success and error
        # scenarios. While we don't need final error processing in this task,
        # it is good practice to catch any final errors for diagnostic purposes.
        dl.addCallback(self._finished)

        # returning a Deferred will keep the framework from assuming the task
        # is done until the Deferred actually completes
        return dl
    

#
# Collector Daemon Main entry point
#
if __name__ == '__main__':
    myPreferences = ZenPerfWmiPreferences()
    myTaskFactory = SimpleTaskFactory(ZenPerfWmiTask)
    myTaskSplitter = SimpleTaskSplitter(myTaskFactory)
    daemon = CollectorDaemon(myPreferences, myTaskSplitter)
    daemon.run()
