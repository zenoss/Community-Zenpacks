from Globals import InitializeClass

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS
from Products.ZenRelations.RelSchema import ToOne, ToManyCont, ToMany
from Products.ZenModel.Device import Device
from Products.ZenUtils.Utils import prepId
#, convToUnits

from Products.CMFCore.utils import getToolByName

import copy
# from AccessControl import ClassSecurityInfo

def manage_createAppEngineApplication(context, applicationId, REQUEST=None):
    """make a AppEngine application"""
    applicationId = prepId(applicationId)
    context._setObject(applicationId, AppEngineApplication(applicationId))
    application = context._getOb(applicationId)
    return application

class AppEngineApplication(Device):
    "An application (also a faux zenoss device) that runs inside google app engine."

    id=''
    applicationname=''
    billing=''
    url=''
    errors=''
    load=''
    ref=''
    hostRef=''
    version=''

    appEngineEntityType='Application'
    meta_type='AppEngineApplication'

    _properties = Device._properties + (
        dict(id='applicationname',   type='string',   mode='w'),
        dict(id='billing',      type='int',      mode='w'),
        dict(id='errors',      type='string',   mode='w'),
        dict(id='load',  type='string',   mode='w'),
        dict(id='ref',         type='string',   mode='w'),
        dict(id='instanceRef',     type='string',   mode='w'),
        dict(id='url',     type='string',   mode='w'),
        dict(id='version',     type='string',   mode='w')
        )

    _relations = Device._relations + (
        ('hostInstance', ToOne(ToManyCont, "ZenPacks.chudler.GoogleAppEngine.AppEngineInstance", "hostedApplications")),
        )

    factory_type_information = (
        {
            'id'             : 'AppEngineApplication',
            'meta_type'      : 'AppEngineApplication',
            'description'    : 'AppEngine Application',
            'icon'           : 'appengine_icon.png',
            'product'        : 'GoogleAppEngine',
            'factory'        : 'manage_addAppEngineApplication',
            'immediate_view' : 'appEngineApplicationStatus',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'appEngineApplicationStatus'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perf'
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

    def name(self):
        return self.applicationname

    def managedDevice(self):
        return None

    def getAdminStatus(self):
        """
        Return 'available' or 'unavailable' depending on the application's
        deployed state.  Available means the application has deployed at
        least one version
        """
        return 'available'

    def index_object(self):
        super(AppEngineApplication, self).index_object()
        try:
            catalog = getToolByName(self, 'appEngineApplicationSearch')
        except AttributeError:
            pass
        else:
            catalog.catalog_object(self, self.getPrimaryId())

    def appEngineStatus(self):
        """

        """
        return self.getAdminStatus()

InitializeClass(AppEngineApplication)
