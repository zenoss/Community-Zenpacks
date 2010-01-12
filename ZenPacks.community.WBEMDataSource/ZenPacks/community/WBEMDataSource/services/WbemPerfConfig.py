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

$Id: WbemPerfConfig.py,v 1.1 2009/12/20 20:26:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenCollector.services.config import CollectorConfigService
from Products.ZenUtils.ZenTales import talesEval

import logging
log = logging.getLogger('zen.ModelerService.WbemPerfConfig')


def getWbemComponentConfig(comp, queries, datapoints):
    threshs = []
    basepath = comp.rrdPath()
    perfServer = comp.device().getPerformanceServer()
    for templ in comp.getRRDTemplates():
        names = []
        for ds in templ.getRRDDataSources("WBEM")+templ.getRRDDataSources("CIM"):
            if not ds.enabled: continue
            transport, classname, kb, namespace = ds.getInstanceInfo(comp)
            if transport is not "WBEM": continue
	    qid = comp.id + "_" + templ.id + "_" + ds.id
	    datapoints[qid] = []
	    properties = {}
	    compname = comp.meta_type == "Device" and "" or comp.id
            for dp in ds.getRRDDataPoints():
                if len(dp.aliases()) > 0:
                    alias = dp.aliases()[0].id
                    expr = talesEval("string:%s"%dp.aliases()[0].formula, comp,
		                                            extra={'now':'now'})
                else:
                    alias = dp.id
                    expr = None
		properties[alias] = dp.id
                dpname = dp.name()
                names.append(dpname)
                datapoints[qid].append((dp.id,
		                        compname,
		                        expr,
                                        "/".join((basepath, dpname)),
                                        dp.rrdtype,
                                        dp.getRRDCreateCommand(perfServer),
                                        (dp.rrdmin, dp.rrdmax)))
            if type(kb) is dict:
                instkey = tuple(sorted(kb.values()))
            else:
                instkey = kb
	    classkey = (namespace, classname)
            if classkey not in queries:
                queries[classkey] = {}
            if type(kb) is dict:
                instkey = tuple(kb.keys())
		instval = tuple(kb.values())
		if instkey not in queries[classkey]:
		    queries[classkey][instkey] = {}
                queries[classkey][instkey][instval] = (qid, properties)
	    else:
                queries[classkey][kb] = (qid, properties)
        for threshold in templ.thresholds():
            if not threshold.enabled: continue
            for ds in threshold.dsnames:
                if ds not in names: continue
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
        CollectorConfigService.__init__(self, dmd, instance,
                                                        deviceProxyAttributes)
        
        
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
