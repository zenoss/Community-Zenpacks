"""Inspired by the Zenoss Enterprise VMware ESX Plugin"""
import md5

import Globals

from DateTime import DateTime
from itertools import chain
from twisted.internet.defer import succeed

from Products.ZenHub.services.Procrastinator import Procrastinate
from Products.ZenHub.services.PerformanceConfig import PerformanceConfig
from Products.ZenUtils.ZenTales import talesCompile
from Products.PageTemplates.Expressions import getEngine

from ZenPacks.chudler.GoogleAppEngine.gaeclient import MetricId
from ZenPacks.chudler.GoogleAppEngine.AppEngineInstanceConfiguration \
        import AppEngineInstanceConfiguration
from twisted.spread import pb


class RRDConfig(pb.Copyable, pb.RemoteCopy):
    """
    RRD configuration for a datapoint.
    Contains the create command and the min and max
    values for a datapoint
    """
    def __init__(self, dp):
        self.dpName = dp.name()
        self.command = dp.createCmd
        self.dataPointId = dp.id
        self.min = dp.rrdmin
        self.max = dp.rrdmax
        self.rrdType = dp.rrdtype

pb.setUnjellyableForClass(RRDConfig, RRDConfig)


class AppEngineDataSourceConfig(pb.Copyable, pb.RemoteCopy):
    """
    Represents the configuration for an individual appengine object.
    """

    def __init__(self, id, datasourceId, metricId, rrdPath,
                 rrdConfig, thresholds, eventKey ):
        self.id = id
        self.datasourceId=datasourceId
        self.metricId = metricId
        self.rrdPath = rrdPath
        self.rrdConfig = rrdConfig
        self.thresholds = thresholds
        self.eventKey = eventKey


pb.setUnjellyableForClass(AppEngineDataSourceConfig, AppEngineDataSourceConfig)


def retrieveDataSourceConfigs( entity ):
    """
    Represents an AppEngine datasource configuration on a device.
    """
    for template in entity.getRRDTemplates():
        for ds in template.getRRDDataSources():
            datapoints=ds.datapoints()
            if ds.sourcetype == 'AppEngine' and len(datapoints) > 0:
                rrdConfig = {}
                for dp in ds.datapoints():
                    rrdConfig[dp.id] = RRDConfig(dp)
                thresholds = []
                for thresh in template.thresholds():
                    thresholds.append(thresh.createThresholdInstance(entity))
                instance = ds.instance
                if not instance.startswith('string:') and \
                   not instance.startswith('python:'):
                    instance = 'string:%s' % instance
                compiled = talesCompile(instance)
                d = entity.device()
                environ = {'dev' : d,
                           'device': d,
                           'devname': d.id,
                           'here' : entity,
                           'nothing' : None,
                           'now' : DateTime() }
                instance = compiled(getEngine().getContext(environ))
                counterId = ds.id
                if counterId==None: continue
                metricId=MetricId(counterId, instance)
                rrdPath='%s/%s' % (entity.rrdPath(), rrdConfig[dp.id].dpName)
                eventKey = ds.eventKey

                yield AppEngineDataSourceConfig(
                                entity.id, ds.id,
                                metricId, rrdPath,
                                rrdConfig, thresholds, eventKey )


def getAppEngineInstanceId( entity ):
    # 0-'' 1-'zport' 2-'dmd' 3-'Devices' 4-'AppEngine' 5-instanceid
    return entity.getPrimaryPath()[5]


def retrieveInstanceConnectionInfo( entity ):
    user = entity.zAppEngineInstanceUser
    password = entity.zAppEngineInstancePassword
    instanceConfig=AppEngineInstanceConfiguration(getAppEngineInstanceId(entity), user,password)
    return instanceConfig

class AppEnginePerfConfigService(PerformanceConfig):
    """ZenHub service for getting AppEngine configurations
       from the object database"""

    def getDeviceConfig(self, device):
        """
        override method from PerformanceConfig
        Returns a hunk of datasources for this device
        """
        connectInfo = retrieveInstanceConnectionInfo( device )
        configGenerators = []
        configGenerators.append( retrieveDataSourceConfigs( device) )
        for comp in device.getMonitoredComponents():
            configGenerators.append( retrieveDataSourceConfigs( comp ) )
        for config in chain( *configGenerators ):
            yield connectInfo, config

    def sendDeviceConfig(self, listener, configs):
        """
        override method from PerformanceConfig.
        Don't send individual device configs because daemons interact
        with instance as a whole.  See L{update}
        """
        return succeed(None)

    def getTargets(self, instanceOrganizers=None, entities=None):
        hasInstances=instanceOrganizers and len(instanceOrganizers) > 0
        hasEntities=False
        if entities:
            hasEntities = len(entities) > 0
        find = self.dmd.Devices.findAppEngineDevices
        perfMonitor = self.instance
        if not hasEntities and not hasInstances:
            for t in find('', performanceMonitor=perfMonitor):
                yield t.primaryAq()
        else:
            if hasEntities:
                for entity in entities:
                    yield self.config.findDevice(entity)
            if hasInstances:
                for instance in instanceOrganizers:
                    for t in find(instance, performanceMonitor=perfMonitor):
                        yield t

    def sendAllDeviceConfigsForInstance( self, instanceId ):
        instanceConfigMap = self.remote_getDeviceConfigs( [instanceId] )
        for listener in self.listeners:
            listener.callRemote( 'updateDeviceConfig', instanceConfigMap )
        return succeed(None)

    def update(self, object):
        from Products.ZenModel.DeviceClass import DeviceClass
        if isinstance( object, DeviceClass ):
            if hasattr( object, 'zAppEngineInstanceUser') and \
                object.__primary_parent__.id == 'AppEngine':
                procrastinator = Procrastinate(
                                        self.sendAllDeviceConfigsForInstance )
                procrastinator.doLater( object.id )
        PerformanceConfig.update( self, object )


    def remote_getDeviceConfigs(self, instanceOrganizers=None, entities=None):
        """
        """
        instanceConfigMap={}
        for target in self.getTargets(instanceOrganizers, entities):
            if target.getProdState() != 'Decommissioned':
                configs = self.getDeviceConfig(target)
                for instance, config in configs:
                    instanceConfigMap.setdefault(instance, []).append(config)
        return instanceConfigMap

