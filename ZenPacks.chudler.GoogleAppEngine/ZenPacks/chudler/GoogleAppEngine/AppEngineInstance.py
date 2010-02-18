"""
TODO 03FEB10:  This version never actually creates this class in the device tree.
  It is not clear yet what would be interesting to see here, besides perhaps
  the Edit tab
"""

from Globals import InitializeClass

import transaction

from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenRelations.RelSchema import ToOne, ToManyCont, ToMany
from Products.ZenModel.Device import Device

connStates={'connected':'Connected',
            'disconnected':'Disconnected',
            'notResponding':'Not responding'}

powerStates={'poweredOff':'Powered off',
             'poweredOn':'Powered on',
             'standBy':'Standby',
             'unknown':'Unknown'}

class AppEngineInstance(Device):
    """A public Google platform and SDK that runs python or java applications.
    An instance can contain many applications."""


    # TODO 03FEB10: Cleanup vestiges
    ref=''
    name=''
    appEngineEntityType='Instance'

    properties = Device._properties + (
        {'id':'ref', 'type':'string', 'mode':'w'},
        {'id':'name', 'type':'string', 'mode':'w'}
        )

    _relations = Device._relations + (
        ('hostedApplications', ToManyCont(ToOne,
            "ZenPacks.chudler.GoogleAppEngine.AppEngineApplication", "hostInstance")),
        )

    factory_type_information = (
        {
            'immediate_view' : 'appEngineInstanceStatus',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'appEngineInstanceStatus'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'osdetail'
                , 'name'          : 'OS'
                , 'action'        : 'deviceOsDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'applications'
                , 'name'          : 'Applicationsk'
                , 'action'        : 'zenAppEngineInstaneDetail'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'hwdetail'
                , 'name'          : 'Hardware'
                , 'action'        : 'deviceHardwareDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'swdetail'
                , 'name'          : 'Software'
                , 'action'        : 'deviceSoftwareDetail'
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


    def getInstance(self):
        return self.getPrimaryPath()[-4]

    def appEngineStatus(self):
	    return 'Something pretty'

InitializeClass(AppEngineInstance)
