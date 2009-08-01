################################################################################
#
# This program is part of the WMIDataSource Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WmiPerfConfig

Provides Wmi config to zenperfwmi clients.

$Id: WmiPerfConfig.py,v 1.1 2009/08/01 02:00:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenWin.services.WmiConfig import *
from Products.ZenHub.PBDaemon import translateError
from Products.ZenHub.services.Procrastinator import Procrastinate

import logging
log = logging.getLogger('zen.ModelerService.WmiPerfConfig')

def getWmiComponentConfig(comp, queries, datapoints):
    threshs = []
    basepath = comp.rrdPath()
    perfServer = comp.device().getPerformanceServer()
    for templ in comp.getRRDTemplates():
        names = []
        for ds in templ.getRRDDataSources("WMI"):
            if not ds.enabled: continue
            wql = ds.getWql(comp)
            if not wql: continue
	    namespace = ds.namespace
	    if not queries.get(namespace, False):
	        queries[namespace] = {}
	        datapoints[namespace] = {}
	    qid = comp.id + "_" + templ.id + "_" + ds.id
	    queries[namespace][qid] = wql
	    datapoints[namespace][qid] = []
	    compname = comp.meta_type != "Device" and "" or ds.id
            for dp in ds.getRRDDataPoints():
                names.append(dp.name())
                dpname = comp.meta_type != "Device" \
                        and comp.viewName() or dp.id
                datapoints[namespace][qid].append(( dpname,
		                            compname,
                                            "/".join((basepath, dp.name())),
                                            dp.rrdtype,
                                            dp.getRRDCreateCommand(perfServer),
                                            (dp.rrdmin, dp.rrdmax)))
        for threshold in templ.thresholds():
            if not threshold.enabled: continue
            for ds in threshold.dsnames:
                if ds in names:
                    threshs.append(threshold.createThresholdInstance(comp))
                    break
    return threshs



class WmiPerfConfig(WmiConfig):

    def __init__(self, dmd, instance):
        WmiConfig.__init__(self, dmd, instance)
        self.config = self.dmd.Monitors.Performance._getOb(self.instance)
        self.procrastinator = Procrastinate(self.push)


    def getDeviceConfigAndWmiDatasources(self, names):
        """Return a list of (devname,user,passwd,namespace,queries,datapoints) 
        """
        deviceProxies = []
        for device in self._monitoredDevices(names):
	    queries = {}
	    datapoints = {}
            threshs = getWmiComponentConfig(device, queries, datapoints)
            for comp in device.getMonitoredComponents():
                threshs.extend(getWmiComponentConfig(comp, queries, datapoints))
            for namespace, query in queries.iteritems():
                proxy = self.createDeviceProxy(device)
                proxy.id = device.getId()
		proxy.namespace = namespace
		proxy.queries = query
		proxy.datapoints = datapoints[namespace]
	        proxy.thresholds = threshs
                if not proxy.queries:
                    log.debug("Device %s skipped because there are no datasources",
                          proxy.id)
                    continue

                deviceProxies.append(proxy)
                log.debug("Device %s added to proxy list", proxy.id)

        return deviceProxies

    @translateError
    def remote_getDeviceConfigAndWmiDatasources(self, names):
        return self.getDeviceConfigAndWmiDatasources(names)

    @translateError
    def remote_getDefaultRRDCreateCommand(self):
        return self.config.getDefaultRRDCreateCommand()
