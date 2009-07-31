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

$Id: zenperfwmi.py,v 1.1 2009/06/29 10:32:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

import time
from twisted.internet import defer
from twisted.python import failure
from twisted.spread import pb

import Globals
from Products.ZenWin.WMIClient import WMIClient
from Products.ZenWin.WinCollector import WinCollector
from Products.ZenUtils.Driver import drive
from Products.ZenUtils.Timeout import timeout
from pysamba.library import WError
from Products.ZenRRD.RRDUtil import RRDUtil
from Products.ZenRRD.Thresholds import Thresholds


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
        return self._wmi.connect(eventContext, self.host, creds, namespace)


class zenperfwmi(WinCollector):

    name = agent = "zenperfwmi"
    whatIDo = 'read the WMI value'
    attributes = WinCollector.attributes + ('perfsnmpCycleInterval',)

    initialServices = ['EventService',
                'ZenPacks.community.WMIDataSource.services.WmiPerfConfig']

    perfsnmpCycleInterval = 300
    thresholds = None
    rrd = None

    def __init__(self):
        WinCollector.__init__(self)
        self.thresholds = Thresholds()

    def processDevice(self, device, timeoutSecs):
        "Send WQL query on a device"
        def cleanup(result=None):
            if isinstance(result, failure.Failure):
                self.deviceDown(device, result.getErrorMessage())
        def inner(driver):
            try:
                if not device.queries:
                    driver.finish(None)
                self.log.info("Scanning %s", device.id)
                wmic = myWMIClient(device)
                yield wmic.connect(namespace=device.namespace)
                driver.next()
                yield wmic.query(device.queries)
                q = driver.next()
		for tableName, data  in q.iteritems():
		    for dp in device.datapoints[tableName]:
		        if dp[0] == 'sysUpTime':
		            value = long(getattr(data[0], 'SystemUpTime', None)) * 100
			else:
		            value = long(getattr(data[0], dp[0], None))
		        self.storeRRD(dp, value)
                wmic.close()
                self.log.info("Finished scanning %s", device.id)
            except WError, ex:
                if ex.werror != 0x000006be:
                    raise
                self.log.info("%s: Ignoring event %s "
                              "and restarting connection", device.id, ex)
                cleanup()
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



    def updateDevices(self, cfg):
        WinCollector.updateDevices(self, cfg)
	for c in cfg:
            self.thresholds.updateForDevice(c.id, c.thresholds)


    def updateConfig(self, cfg):
        WinCollector.updateConfig(self, cfg)
        self.heartbeatTimeout = self.perfsnmpCycleInterval * 3

    def configService(self):
        """
        Gather this daemons WMI configuration
        
        @return: zenhub configuration information
        @rtype: WmiPefConfig
        """
        return self.services.get('ZenPacks.community.WMIDataSource.services.WmiPerfConfig')

    def fetchDevices(self, driver):
        yield self.configService().callRemote('getThresholdClasses')
        self.remote_updateThresholdClasses(driver.next())

        yield self.configService().callRemote('getDeviceListByMonitor',
                                              self.options.monitor)

        yield self.configService().callRemote('getDeviceConfigAndWmiDatasources', 
                                              driver.next())

        self.updateDevices(driver.next())

        yield self.configService().callRemote('getDefaultRRDCreateCommand')
        createCommand = driver.next()

        self.rrd = RRDUtil(createCommand, self.perfsnmpCycleInterval)


    def cycleInterval(self):
        return self.perfsnmpCycleInterval


if __name__ == "__main__":
    from ZenPacks.community.WMIDataSource.zenperfwmi import zenperfwmi
    zw = zenperfwmi()
    zw.run()
