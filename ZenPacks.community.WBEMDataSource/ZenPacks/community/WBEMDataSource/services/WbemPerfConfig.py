################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WbemPerfConfig

Provides Wbem config to zenperfwmi clients.

$Id: WbemPerfConfig.py,v 1.0 2009/07/25 00:34:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenCollector.services.config import CollectorConfigService

import logging
log = logging.getLogger('zen.ModelerService.WbemPerfConfig')

def getWbemComponentConfig(comp, queries, datapoints):
    threshs = []
    basepath = comp.rrdPath()
    perfServer = comp.device().getPerformanceServer()
    for templ in comp.getRRDTemplates():
        names = []
        for ds in templ.getRRDDataSources("WBEM"):
            if not ds.enabled: continue
            instanceName = ds.getInstanceName(comp)
            if not instanceName: continue
	    qid = comp.id + "_" + templ.id + "_" + ds.id
	    datapoints[qid] = []
	    compname = comp.meta_type != "Device" and "" or ds.id
	    propertyList = []
            for dp in ds.getRRDDataPoints():
                names.append(dp.name())
                propertyList.append(dp.id)
                dpname = comp.meta_type != "Device" \
                        and comp.viewName() or dp.id
                datapoints[qid].append(( dpname,
		                        compname,
                                        "/".join((basepath, dp.name())),
                                        dp.rrdtype,
                                        dp.getRRDCreateCommand(perfServer),
                                        (dp.rrdmin, dp.rrdmax)))
	    queries[qid] =  instanceName + (propertyList, )
        for threshold in templ.thresholds():
            if not threshold.enabled: continue
            for ds in threshold.dsnames:
                if ds in names:
                    threshs.append(threshold.createThresholdInstance(comp))
                    break
    return threshs


class WbemPerfConfig(CollectorConfigService):
    
    def __init__(self, dmd, instance):
        deviceProxyAttributes = ('zWinUser',
                                 'zWinPassword',
                                 'zWbemUseSSL',
                                 'zWbemPort',
				 'zWbemProxy')
        CollectorConfigService.__init__(self, dmd, instance, deviceProxyAttributes)
        
        
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
        
        threshs = getWbemComponentConfig(device, queries, datapoints)
        for comp in device.getMonitoredComponents():
            threshs.extend(getWbemComponentConfig(comp, queries, datapoints))
	proxy.queries = queries
	proxy.datapoints = datapoints
	proxy.thresholds = threshs
        if not proxy.queries:
            log.debug("Device %s skipped because there are no datasources",
                          device.getId())
            return None
                
        return proxy
