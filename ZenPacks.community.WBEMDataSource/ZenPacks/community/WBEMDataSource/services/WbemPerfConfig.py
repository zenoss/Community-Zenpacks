################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WbemPerfConfig

Provides Wbem config to zenperfwbem clients.

$Id: WbemPerfConfig.py,v 1.7 2010/05/20 21:14:27 egor Exp $"""

__version__ = "$Revision: 1.7 $"[11:-2]

from Products.ZenCollector.services.config import CollectorConfigService
from Products.ZenUtils.ZenTales import talesEval

import logging
log = logging.getLogger('zen.ModelerService.WbemPerfConfig')


def sortQuery(qs, table, query):
    cn, kbs, ns, props = query
    if not kbs: kbs = {}
    ikey = tuple(kbs.keys())
    ival = tuple(kbs.values())
    try:
        if ival not in qs[ns][cn][ikey]:
            qs[ns][cn][ikey][ival] = []
        qs[ns][cn][ikey][ival].append((table, props))
    except KeyError:
        try:
            qs[ns][cn][ikey] = {}
        except KeyError:
            try:
                qs[ns][cn] = {}
            except KeyError:
                qs[ns] = {}
                qs[ns][cn] = {}
            qs[ns][cn][ikey] = {}
        qs[ns][cn][ikey][ival] = [(table, props)]
    return qs


def getWbemComponentConfig(transports, comp, queries, datapoints):
    threshs = []
    basepath = comp.rrdPath()
    perfServer = comp.device().getPerformanceServer()
    for templ in comp.getRRDTemplates():
        names = []
        datasources = []
        for tr in transports:
            datasources.extend(templ.getRRDDataSources(tr))
        for ds in datasources:
            if not ds.enabled: continue
            transport, classname, kb, namespace = ds.getInstanceInfo(comp)
            if transport != transports[0]: continue
            qid = comp.id + "_" + templ.id + "_" + ds.id
            datapoints[qid] = []
            properties = {}
            compname = comp.meta_type == "Device" and "" or comp.id
            for dp in ds.getRRDDataPoints():
                if len(dp.aliases()) > 0:
                    alias = dp.aliases()[0].id.strip()
                    expr = talesEval("string:%s"%dp.aliases()[0].formula, comp,
                                                            extra={'now':'now'})
                else:
                    alias = dp.id.strip()
                    expr = None
                if alias not in properties: properties[alias] = (dp.id,)
                else: properties[alias] = properties[alias] + (dp.id,)
                dpname = dp.name()
                names.append(dpname)
                datapoints[qid].append((dp.id,
                                        compname,
                                        expr,
                                        "/".join((basepath, dpname)),
                                        dp.rrdtype,
                                        dp.getRRDCreateCommand(perfServer),
                                        (dp.rrdmin, dp.rrdmax)))
            queries = sortQuery(queries,qid,(classname,kb,namespace,properties))
        for threshold in templ.thresholds():
            if not threshold.enabled: continue
            for ds in threshold.dsnames:
                if ds not in names: continue
                threshs.append(threshold.createThresholdInstance(comp))
                break
    return threshs


def getWbemDeviceConfig(trs, device):
    queries = {}
    datapoints = {}
    threshs = getWbemComponentConfig(trs, device, queries, datapoints)
    for comp in device.getMonitoredComponents():
        threshs.extend(getWbemComponentConfig(trs, comp, queries, datapoints))
    return queries, datapoints, threshs


class WbemPerfConfig(CollectorConfigService):

    def __init__(self, dmd, instance):
        self.cimtransport = ['WBEM', 'CIM']
        deviceProxyAttributes = ('zWbemMonitorIgnore',
                                 'zWbemUseSSL',
                                 'zWbemPort',
                                 'zWbemProxy',
                                 'zWinUser',
                                 'zWinPassword')
        CollectorConfigService.__init__(self, dmd, instance,
                                                        deviceProxyAttributes)

    def _filterDevice(self, device):
        include = CollectorConfigService._filterDevice(self, device)
        zIgnore = 'z%s%sMonitorIgnore'%(self.cimtransport[0][0].upper(),
                                        self.cimtransport[0][1:].lower()) 
        if getattr(device, zIgnore, False):
            log.debug("Device %s skipped because %s is True", device.id,zIgnore)
            include = False
        return include

    def _createDeviceProxy(self, device):
        proxy = CollectorConfigService._createDeviceProxy(self, device)

        # for now, every device gets a single configCycleInterval based upon
        # the collector's winCycleInterval configuration which is typically
        # located at dmd.Monitors.Performance._getOb('localhost').
        # TODO: create a zProperty that allows for individual device schedules
        proxy.configCycleInterval = self._prefs.perfsnmpCycleInterval
        proxy.queries, proxy.datapoints, proxy.thresholds = getWbemDeviceConfig(
                                                            self.cimtransport,
                                                            device)
        if not proxy.queries:
            log.debug("Device %s skipped because there are no datasources",
                          device.getId())
            return None
        return proxy
