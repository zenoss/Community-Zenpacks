################################################################################
#
# This program is part of the SQLDataSource Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SqlPerfConfig

Provides config to zenperfsql clients.

$Id: SqlPerfConfig.py,v 1.1 2010/11/22 20:00:17 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenCollector.services.config import CollectorConfigService
from Products.ZenUtils.ZenTales import talesEval
from ZenPacks.community.SQLDataSource.datasources.SQLDataSource \
    import SQLDataSource as DataSource

import logging
log = logging.getLogger('zen.SqlPerfConfig')


def sortQuery(qs, table, query):
    sql, kbs, cs, cols = query
    if not kbs: kbs = {}
    ikey = tuple(kbs.keys())
    ival = tuple(kbs.values())
    try:
        if ival not in qs[cs][sql][ikey]:
            qs[cs][sql][ikey][ival] = []
        qs[cs][sql][ikey][ival].append((table, cols))
    except KeyError:
        try:
            qs[cs][sql][ikey] = {}
        except KeyError:
            try:
                qs[cs][sql] = {}
            except KeyError:
                qs[cs] = {}
                qs[cs][sql] = {}
            qs[cs][sql][ikey] = {}
        qs[cs][sql][ikey][ival] = [(table, cols)]
    return qs


def getSqlComponentConfig(comp, queries, datapoints):
    threshs = []
    try:
        basepath = comp.rrdPath()
        perfServer = comp.device().getPerformanceServer()
    except: return []
    for templ in comp.getRRDTemplates():
        names = []
        for ds in templ.getRRDDataSources():
            if not ds.enabled: continue
            if not isinstance(ds, DataSource): continue
            qi = ds.getQueryInfo(comp)
            if not qi: continue
            qid = comp.id + "_" + templ.id + "_" + ds.id
            datapoints[qid] = []
            columns = {}
            compname = comp.meta_type == "Device" and "" or comp.id
            for dp in ds.getRRDDataPoints():
                if len(dp.aliases()) > 0:
                    alias = dp.aliases()[0].id.strip()
                    expr = talesEval("string:%s"%dp.aliases()[0].formula, comp,
                                                            extra={'now':'now'})
                else:
                    alias = dp.id.strip()
                    expr = None
                if alias not in columns: columns[alias] = (dp.id,)
                else: columns[alias] = columns[alias] + (dp.id,)
                dpname = dp.name()
                names.append(dpname)
                datapoints[qid].append((dp.id,
                                        compname,
                                        expr,
                                        "/".join((basepath, dpname)),
                                        dp.rrdtype,
                                        dp.getRRDCreateCommand(perfServer),
                                        (dp.rrdmin, dp.rrdmax)))
            queries = sortQuery(queries, qid, qi + (columns,))
        for threshold in templ.thresholds():
            if not threshold.enabled: continue
            for ds in threshold.dsnames:
                if ds not in names: continue
                threshs.append(threshold.createThresholdInstance(comp))
                break
    return threshs


def getSqlDeviceConfig(device):
    queries = {}
    datapoints = {}
    threshs = getSqlComponentConfig(device, queries, datapoints)
    for comp in device.getMonitoredComponents():
        threshs.extend(getSqlComponentConfig(comp, queries, datapoints))
    return queries, datapoints, threshs


class SqlPerfConfig(CollectorConfigService):

    def _createDeviceProxy(self, device):
        proxy = CollectorConfigService._createDeviceProxy(self, device)

        # for now, every device gets a single configCycleInterval based upon
        # the collector's winCycleInterval configuration which is typically
        # located at dmd.Monitors.Performance._getOb('localhost').
        # TODO: create a zProperty that allows for individual device schedules
        proxy.configCycleInterval = self._prefs.perfsnmpCycleInterval
        proxy.queries, proxy.datapoints, proxy.thresholds = getSqlDeviceConfig(
                                                                        device)
        if not proxy.queries:
            log.debug("Device %s skipped because there are no datasources",
                          device.getId())
            return None
        return proxy
