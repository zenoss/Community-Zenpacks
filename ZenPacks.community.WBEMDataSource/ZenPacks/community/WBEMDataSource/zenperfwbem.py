################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""zenperfwbem

Gets WBEM performance data and stores it in RRD files.

$Id: zenperfwbem.py,v 1.0 2009/07/25 00:35:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

import time
import datetime
from twisted.internet import defer
from twisted.python import failure
from twisted.spread import pb

import Globals
from WBEMClient import WBEMClient
from ZenPacks.community.WBEMDataSource.lib.pywbem import CIMDateTime, CIMError
from ZenPacks.community.WBEMDataSource.WBEMCollector import WBEMCollector
from Products.ZenUtils.Driver import drive
from Products.ZenUtils.Timeout import timeout
from Products.ZenRRD.RRDUtil import RRDUtil
from Products.ZenRRD.Thresholds import Thresholds


class zenperfwbem(WBEMCollector):

    name = agent = "zenperfwbem"
    whatIDo = 'read the WBEM value'

    perfsnmpCycleInterval = 300
    thresholds = None
    rrd = None

    def __init__(self):
        WBEMCollector.__init__(self)
        self.thresholds = Thresholds()

    def processDevice(self, device, timeoutSecs):
        "Get WBEM Instances"
        def cleanup(result=None):
            if isinstance(result, failure.Failure):
                self.deviceDown(device, result.getErrorMessage())
        def inner(driver):
            try:
                if not device.queries:
                    driver.finish(None)
                self.log.info("Scanning %s", device.id)
                wbemc = WBEMClient(device)
                yield wbemc.query(device.queries)
                q = driver.next()
		for tableName, data  in q.iteritems():
		    for dp in device.datapoints[tableName]:
		        if isinstance(data[dp[0]], CIMDateTime):
		            t = data[dp[0]].datetime
		            value=time.mktime(t.timetuple())+1e-6*t.microsecond     
		        if dp[0] == 'LastBootUpTime':
		            value= round((time.time() - value) * 100)
		            newpath=dp[2].replace('OperatingSystem_LastBootUpTime',
		                                    'sysUpTime_sysUpTime') 
		            ndp = (dp[0], dp[1], newpath, dp[3], dp[4], dp[5])
		            self.storeRRD(ndp, value)
			else:
		            value = long(data[dp[0]])
		            self.storeRRD(dp, value)
                self.log.info("Finished scanning %s", device.id)
            except CIMError, ex:
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
        WBEMCollector.updateDevices(self, cfg)
	for c in cfg:
            self.thresholds.updateForDevice(c.id, c.thresholds)


    def updateConfig(self, cfg):
        WBEMCollector.updateConfig(self, cfg)
        self.heartbeatTimeout = self.perfsnmpCycleInterval * 3


    def fetchDevices(self, driver):
        yield self.configService().callRemote('getThresholdClasses')
        self.remote_updateThresholdClasses(driver.next())

        yield self.configService().callRemote('getDeviceListByMonitor',
                                              self.options.monitor)

        yield self.configService().callRemote('getDeviceConfigAndWbemDatasources', 
                                              driver.next())

        self.updateDevices(driver.next())

        yield self.configService().callRemote('getDefaultRRDCreateCommand')
        createCommand = driver.next()

        self.rrd = RRDUtil(createCommand, self.perfsnmpCycleInterval)


    def cycleInterval(self):
        return self.perfsnmpCycleInterval


if __name__ == "__main__":
    from ZenPacks.community.WBEMDataSource.zenperfwbem import zenperfwbem
    zw = zenperfwbem()
    zw.run()
