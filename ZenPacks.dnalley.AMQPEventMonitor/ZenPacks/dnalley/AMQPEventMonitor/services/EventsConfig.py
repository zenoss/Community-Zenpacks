from Acquisition import aq_base
from Products.ZenCollector.services.config import CollectorConfigService

class EventsConfig(CollectorConfigService):
    def __init__(self, dmd, instance):
        dpAttr = ('zAMQPPort', 'zAMQPUsername', 'zAMQPPassword',
                  'zAMQPVirtualHost', 'zAMQPQueue', 'zAMQPIgnore')
        CollectorConfigService.__init__(self, dmd, instance, dpAttr)

    def _filterDevice(self, device):
        return CollectorConfigService._filterDevice(self, device) and not getattr(device, 'zAMQPIgnore', True)

    def _createDeviceProxy(self, device):
        proxy = CollectorConfigService._createDeviceProxy(self, device)
        proxy.configCycleInterval = 5 * 60
        return proxy