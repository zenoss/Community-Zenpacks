################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OdbcPerfConfig

Provides config to zenperfodbc clients.

$Id: OdbcPerfConfig.py,v 2.1 2009/11/09 13:28:23 egor Exp $"""

__version__ = "$Revision: 2.1 $"[11:-2]


from Products.ZenCollector.services.config import CollectorConfigService

import logging
log = logging.getLogger('zen.ModelerService.OdbcPerfConfig')

def getOdbcComponentConfig(comp, queries, datapoints):
    threshs = []
    basepath = comp.rrdPath()
    perfServer = comp.device().getPerformanceServer()
    for templ in comp.getRRDTemplates():
        names = []
        for ds in templ.getRRDDataSources("ODBC"):
            if not ds.enabled: continue
	    qid = comp.id + "_" + templ.id + "_" + ds.id
	    queries[qid] =  ds.getQuery(comp)
            if not queries[qid]: continue
	    datapoints[qid] = []
	    compname = comp.meta_type != "Device" and comp.id or ds.id
            for dp in ds.getRRDDataPoints():
                names.append(dp.name())
                datapoints[qid].append((dp.id,
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


class OdbcPerfConfig(CollectorConfigService):
    
    def _createDeviceProxy(self, device):
	queries = {}
	datapoints = {}
        proxy = CollectorConfigService._createDeviceProxy(self, device)
	proxy.thresholds = []
        
        # for now, every device gets a single configCycleInterval based upon
        # the collector's winCycleInterval configuration which is typically
        # located at dmd.Monitors.Performance._getOb('localhost').
        # TODO: create a zProperty that allows for individual device schedules
        proxy.configCycleInterval = self._prefs.configCycleInterval
        
        threshs = getOdbcComponentConfig(device, queries, datapoints)
        for comp in device.getMonitoredComponents():
            threshs.extend(getOdbcComponentConfig(comp, queries, datapoints))
	proxy.queries = queries
	proxy.datapoints = datapoints
	proxy.thresholds = threshs
        if not proxy.queries:
            log.debug("Device %s skipped because there are no datasources",
                          device.getId())
            return None
                
        return proxy
