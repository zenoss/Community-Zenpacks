###############################################################################
#
# EnvironmentAlert object class
#
###############################################################################

__doc__ = """ EnvironmentAlert

EnvironmentAlert is a component of a SerialConsoleDevice

$id: $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class EnvironmentAlert(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'EnvironmentAlert'

    ogEnvAlertStatusIndex = -1
    ogEnvAlertStatusDevice = ""
    ogEnvAlertStatusSensor = ""
    ogEnvAlertStatusOutlet = -1
    ogEnvAlertStatusValue = -1
    ogEnvAlertStatusOldValue = -1
    ogEnvAlertStatusStatus = 0
    snmpindex = -1

    _properties = (
        dict(id = 'ogEnvAlertStatusIndex',     type = 'int',    **_kw),
        dict(id = 'ogEnvAlertStatusDevice',    type = 'string', **_kw),
        dict(id = 'ogEnvAlertStatusSensor',    type = 'string', **_kw),
        dict(id = 'ogEnvAlertStatusOutlet',    type = 'int',	**_kw),
        dict(id = 'ogEnvAlertStatusValue',     type = 'int',	**_kw),
        dict(id = 'ogEnvAlertStatusOldValue',  type = 'int',	**_kw),
        dict(id = 'ogEnvAlertStatusStatus',    type = 'int',    **_kw),
    )

    _relations = (
        ('SerialConsoleDev',
            ToOne(ToManyCont,
            'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
            'EnvironmentAlrt')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'EnvironmentAlert',
        'meta_type'      : 'EnvironmentAlert',
        'description'    : 'Opengear EMD Alert info',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addEnvironmentAlert',
        'immediate_view' : 'environmentAlertPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'environmentAlertPerformance',
            'permissions'   : (ZEN_VIEW, )
        }, {
            'id'            : 'templates',
            'name'          : 'Templates',
            'action'        : 'objTemplates',
            'permissions'   : (ZEN_CHANGE_SETTINGS, )
        },)
    },)

    def device(self):
        return self.SerialConsoleDev()

    def managedDeviceLink(self):
        #from Products.ZenModel.ZenModelRM import ZenModelRM
        #d = self.getDmdRoot("Devices").findDevice(self.serverAlias)
        #if d:
        #    return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

InitializeClass(EnvironmentAlert)
