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

$Id: OdbcPlugin.py,v 2.1 2009/11/09 12:41:23 egor Exp $"""

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
from Products.ZenEvents.ZenEventClasses import Error, Clear
from Products.ZenUtils.observable import ObservableMixin
from OdbcClient import OdbcClient, CError

# We retrieve our configuration data remotely via a Twisted PerspectiveBroker
# connection. To do so, we need to import the class that will be used by the
# configuration service to send the data over, i.e. DeviceProxy.
from Products.ZenUtils.Utils import unused
from Products.ZenCollector.services.config import DeviceProxy
unused(DeviceProxy)

#
# creating a logging context for this module to use
#
log = logging.getLogger("zen.zenperfodbc")


# Create an implementation of the ICollectorPreferences interface so that the
# ZenCollector framework can configure itself from our preferences.
class ZenPerfOdbcPreferences(object):
    zope.interface.implements(ICollectorPreferences)
    
    def __init__(self):
        """
        Construct a new ZenPerfOdbcPreferences instance and provide default
        values for needed attributes.
        """
        self.collectorName = "zenperfodbc"
        self.defaultRRDCreateCommand = None
        self.cycleInterval = 5 * 60 # seconds
        self.configCycleInterval = 20 # minutes
        self.options = None
        
        # the configurationService attribute is the fully qualified class-name
        # of our configuration service that runs within ZenHub
        self.configurationService = 'ZenPacks.community.ZenODBC.services.OdbcPerfConfig'
        
        
    def buildOptions(self, parser):
        parser.add_option('--debug', dest='debug', default=False,
                               action='store_true',
                               help='Increase logging verbosity.')

    def postStartup(self):
        # turn on low-level pysamba debug logging if requested
        logseverity = self.options.logseverity


class ZenPerfOdbcTask(ObservableMixin):
    zope.interface.implements(IScheduledTask)
        
    STATE_ODBC_CONNECT = 'ODBC_CONNECT'
    STATE_ODBC_QUERY = 'ODBC_QUERY'
    STATE_ODBC_PROCESS = 'ODBC_PROCESS'
    
    def __init__(self,
                 deviceId,
                 taskName,
                 scheduleIntervalSeconds,
                 taskConfig):
        """
        Construct a new task instance to get ODBC data.
        
        @param deviceId: the Zenoss deviceId to watch
        @type deviceId: string
        @param taskName: the unique identifier for this task
        @type taskName: string
        @param scheduleIntervalSeconds: the interval at which this task will be
               collected
        @type scheduleIntervalSeconds: int
        @param taskConfig: the configuration for this task
        """
        super(ZenPerfOdbcTask, self).__init__()
        
        self.name = taskName
        self.configId = deviceId
        self.interval = scheduleIntervalSeconds
        self.state = TaskStates.STATE_IDLE
        
        self._taskConfig = taskConfig
        self._devId = deviceId
        self._manageIp = self._taskConfig.manageIp
        self._queries = self._taskConfig.queries
        self._thresholds = self._taskConfig.thresholds
        self._datapoints = self._taskConfig.datapoints
        
        self._dataService = zope.component.queryUtility(IDataService)
        self._eventService = zope.component.queryUtility(IEventService)
        self._preferences = zope.component.queryUtility(ICollectorPreferences,
                                                        "zenperfodbc")
	self._odbcc = None
                                                        
    def _finished(self, result):
        """
        Callback activated when the task is complete so that final statistics
        on the collection can be displayed.
        """

        if not isinstance(result, Failure):
            log.debug("Device %s [%s] scanned successfully",
                      self._devId, self._manageIp)
        else:
            log.debug("Device %s [%s] scanned failed, %s",
                      self._devId, self._manageIp, result.getErrorMessage())

        # give the result to the rest of the callback/errchain so that the
        # ZenCollector framework can keep track of the success/failure rate
        return result

    def _failure(self, result):
        """
        Errback for an unsuccessful asynchronous connection or collection 
        request.
        """
        err = result.getErrorMessage()
        log.error("Unable to scan device %s: %s", self._devId, err)

        summary = """
	    Could not fetch data from ODBC source (%s). Check
	    your username/password settings and verify network
	    connectivity.
            """ % err

        self._eventService.sendEvent(dict(
            summary=summary,
            component='zenperfodbc',
            eventClass='/Status/Odbc',
            device=self._devId,
            severity=Error,
            agent='zenperfodbc',
            ))

        # give the result to the rest of the errback chain
        return result


    def _collectSuccessful(self, results):
        """
        Callback for a successful fetch of services from the remote device.
        """
        self.state = ZenPerfOdbcTask.STATE_ODBC_PROCESS
        
        log.debug("Successful collection from %s [%s], results=%s",
                  self._devId, self._manageIp, results)
        
	if results:          
	    for tableName, data in results.iteritems():
		if isinstance(data[0], CError):
		    component = self._datapoints[tableName][0][1]
                    if not component:
                        component = 'zenperfodbc'
                    summary = """
		        Could not fetch data from ODBC source (%s). Check
			your username/password settings and verify network
			connectivity.
		        """ % data[0].getErrorMessage()
                    self._eventService.sendEvent(dict(
            	                                    summary=summary,
            	                                    component=component,
            	                                    eventClass='/Status/Odbc',
            	                                    device=self._devId,
            	                                    severity=Error,
            	                                    agent='zenperfodbc',
            	                                    ))
		    continue
		if not data:
		    component = self._datapoints[tableName][0][1]
                    if not component:
                        component = 'zenperfodbc'
                    summary = 'Database %s is Unavailable.'%component
                    self._eventService.sendEvent(dict(
            	                                    summary=summary,
            	                                    component=component,
            	                                    eventClass='/Status/Odbc',
            	                                    device=self._devId,
            	                                    severity=Error,
            	                                    agent='zenperfodbc',
            	                                    ))
		    continue
		for (dpname, comp, rrdPath, rrdType, rrdCreate,
		                        minmax) in self._datapoints[tableName]:
		    value = data[0].get(dpname, None)
		    if value:
                        self._dataService.writeRRD( rrdPath,
                                                    value,
                                                    rrdType,
			                            rrdCreate,
                                                    min=minmax[0],
                                                    max=minmax[1])
                self._eventService.sendEvent(dict(
            	                        summary='Database %s is Active.' % comp,
            	                        component=comp,
            	                        eventClass='/Status/Odbc',
            	                        device=self._devId,
            	                        severity=Clear,
            	                        agent='zenperfodbc',
            	                        ))
            self._eventService.sendEvent(dict(
            	                summary='Odbc connection to %s up.'%self._devId,
            	                component='zenperfodbc',
            	                eventClass='/Status/Odbc',
            	                device=self._devId,
            	                severity=Clear,
            	                agent='zenperfodbc',
            	                ))
	return results

    def _collectData(self):
        """
        Callback called after a connect or previous collection so that another
        collection can take place.
        """
        log.debug("Polling for ODBC data from %s [%s]", 
                  self._devId, self._manageIp)

        self.state = ZenPerfOdbcTask.STATE_ODBC_QUERY
        odbcc = OdbcClient(self._taskConfig)
	d = odbcc.query(self._queries)
        d.addCallbacks(self._collectSuccessful, self._failure)
        return d
	

    def cleanup(self):
        pass


    def doTask(self):
        log.debug("Scanning device %s [%s]", self._devId, self._manageIp)
        
        # try collecting events after a successful connect, or if we're
        # already connected
	
        d = self._collectData()

        # Add the _finished callback to be called in both success and error
        # scenarios. While we don't need final error processing in this task,
        # it is good practice to catch any final errors for diagnostic purposes.
        d.addCallback(self._finished)

        # returning a Deferred will keep the framework from assuming the task
        # is done until the Deferred actually completes
        return d
    

#
# Collector Daemon Main entry point
#
if __name__ == '__main__':
    myPreferences = ZenPerfOdbcPreferences()
    myTaskFactory = SimpleTaskFactory(ZenPerfOdbcTask)
    myTaskSplitter = SimpleTaskSplitter(myTaskFactory)
    daemon = CollectorDaemon(myPreferences, myTaskSplitter)
    daemon.run()
