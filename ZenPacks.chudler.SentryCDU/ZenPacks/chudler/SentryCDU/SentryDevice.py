from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenRelations.RelSchema import *

import copy
import logging

class SentryDevice(Device):
    "Sentry Cabinet Distribution Unit"

    _relations = Device._relations + ( ("towers", ToManyCont(ToOne, "ZenPacks.chudler.SentryCDU.Tower", "sentrydevice")),
                                       ("sentrysensors", ToManyCont(ToOne, "ZenPacks.chudler.SentryCDU.SentrySensor", "sentrydevice")),
    )
    
    factory_type_information = (
        {
            'immediate_view' : 'deviceStatus',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'deviceStatus'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'osdetail'
                , 'name'          : 'OS'
                , 'action'        : 'deviceOsDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'towerData'
                , 'name'          : 'CDU Hardware'
                , 'action'        : 'towerData'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'hwdetail'
                , 'name'          : 'Hardware'
                , 'action'        : 'deviceHardwareDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfServer'
                , 'name'          : 'Perf'
                , 'action'        : 'viewDevicePerformance'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'edit'
                , 'name'          : 'Edit'
                , 'action'        : 'editDevice'
                , 'permissions'   : ("Change Device",)
                },
            )
         },
        )

    # this is used in a command template to put total tower load in a graph.
    def aggregateLoad(self):
	log = logging.getLogger('zen.ZenEvent')
	log.error('SENTRY: Getting aggregate load for the entire device')
        total = 0
        for tower in self.towers():
            amps = tower.aggregateLoadInt()
            if amps:
                total += amps
	log.error('SENTRY: Done walking the loads for the entire device: %s' % total)
        return '/bin/echo -n "OK|load=%s;;;;"' % (total)

InitializeClass(SentryDevice)
