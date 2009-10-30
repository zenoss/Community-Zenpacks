################################################################################
#
# This program is part of the WMIDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WmiPerfConfig

Provides Wmi config to zenperfwmi clients.

$Id: WmiPerfConfig.py,v 2.1 2009/10/30 17:06:22 egor Exp $"""

__version__ = "$Revision: 2.1 $"[11:-2]

from Products.ZenCollector.services.config import CollectorConfigService

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
	    if ds.namespace not in queries:
	        queries[ds.namespace] = {}
	    qid = comp.id + "_" + templ.id + "_" + ds.id
	    queries[ds.namespace][qid] = wql
	    datapoints[qid] = []
	    compname = comp.meta_type != "Device" and "" or ds.id
            for dp in ds.getRRDDataPoints():
                names.append(dp.name())
                dpname = comp.meta_type != "Device" \
                        and comp.viewName() or dp.id
                datapoints[qid].append(( dpname,
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




class WmiPerfConfig(CollectorConfigService):
    
    def __init__(self, dmd, instance):
        deviceProxyAttributes = ('zWmiMonitorIgnore',
                                 'zWinUser',
                                 'zWinPassword')
        CollectorConfigService.__init__(self, dmd, instance, deviceProxyAttributes)
        
    def _filterDevice(self, device):
        include = CollectorConfigService._filterDevice(self, device)
        
        if getattr(device, 'zWmiMonitorIgnore', False):
            self.log.debug("Device %s skipped because zWmiMonitorIgnore is True",
                           device.id)
            include = False
        return include
        
    def _createDeviceProxy(self, device):
	queries = {}
	datapoints = {}
        proxy = CollectorConfigService._createDeviceProxy(self, device)
	proxy.thresholds = []
        
        # for now, every device gets a single configCycleInterval based upon
        # the collector's winCycleInterval configuration which is typically
        # located at dmd.Monitors.Performance._getOb('localhost').
        # TODO: create a zProperty that allows for individual device schedules
        proxy.configCycleInterval = self._prefs.winCycleInterval
        
        threshs = getWmiComponentConfig(device, queries, datapoints)
        for comp in device.getMonitoredComponents():
            threshs.extend(getWmiComponentConfig(comp, queries, datapoints))
	proxy.queries = queries
	proxy.datapoints = datapoints
	proxy.thresholds = threshs
        if not proxy.queries:
            log.debug("Device %s skipped because there are no datasources",
                          device.getId())
            return None
                
        return proxy
        
