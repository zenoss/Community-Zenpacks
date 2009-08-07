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


from Products.ZenHub.services.ModelerService import ModelerService
from Products.ZenModel.Device import Device

from Products.ZenHub.services.Procrastinator import Procrastinate
from Products.ZenHub.services.ThresholdMixin import ThresholdMixin
from Products.ZenHub.PBDaemon import translateError

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



class WbemPerfConfig(ModelerService, ThresholdMixin):


    def __init__(self, dmd, instance):
        ModelerService.__init__(self, dmd, instance)
        self.config = self.dmd.Monitors.Performance._getOb(self.instance)
        self.procrastinator = Procrastinate(self.pushConfig)


    def createDeviceProxy(self, dev):
        result = ModelerService.createDeviceProxy(self, dev)
        for prop in (
            'zWinUser',
            'zWinPassword',
            'zWbemUseSSL',
            'zWbemPort'):
            if hasattr(dev, prop):
                setattr(result, prop, getattr(dev, prop))
        return result


    def remote_getConfig(self):
        return self.config.propertyItems()


    def update(self, object):
        from Products.ZenModel.RRDDataSource import RRDDataSource
        if isinstance(object, RRDDataSource):
            if object.sourcetype != 'WBEM':
                return
        ModelerService.update(self, object)


    def deleted(self, obj):
        for listener in self.listeners:
            if isinstance(obj, Device):
                listener.callRemote('deleteDevice', obj.id)


    def getDeviceConfigAndWbemDatasources(self, names):
        """Get the WBEM configuration for all devices. 
        """
        deviceProxies = []
        for device in self.config.devices():
            if names and device.id not in names: continue
            device = device.primaryAq()
	    queries = {}
	    datapoints = {}
            threshs = getWbemComponentConfig(device, queries, datapoints)
            for comp in device.getMonitoredComponents():
                threshs.extend(getWbemComponentConfig(comp, queries, datapoints))
            proxy = self.createDeviceProxy(device)
            proxy.id = device.getId()
	    proxy.queries = queries
	    proxy.datapoints = datapoints
	    proxy.thresholds = threshs
            if not proxy.queries:
                log.debug("Device %s skipped because there are no datasources",
                    proxy.id)
                continue
            deviceProxies.append(proxy)
            log.debug("Device %s added to proxy list", proxy.id)
        return deviceProxies

    @translateError
    def remote_getDeviceConfigAndWbemDatasources(self, names):
        return self.getDeviceConfigAndWbemDatasources(names)

    @translateError
    def remote_getDefaultRRDCreateCommand(self):
        return self.config.getDefaultRRDCreateCommand()
