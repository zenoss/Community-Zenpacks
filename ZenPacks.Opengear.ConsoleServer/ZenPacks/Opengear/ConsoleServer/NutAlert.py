###############################################################################
#
# NutAlert object class
#
###############################################################################

__doc__ = """ NutAlert

NutAlert is a component of a SerialConsoleDevice

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

class NutAlert(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'NutAlert'

    ogNutAlertStatusIndex = -1
    ogNutAlertStatusPort = -1
    ogNutAlertStatusName = ""
    ogNutAlertStatusHost = ""
    ogNutAlertStatusStatus = ""
    snmpindex = -1

    _properties = (
        dict(id = 'ogNutAlertStatusIndex',  type = 'int',    **_kw),
        dict(id = 'ogNutAlertStatusPort',   type = 'int',    **_kw),
        dict(id = 'ogNutAlertStatusName',   type = 'string', **_kw),
        dict(id = 'ogNutAlertStatusHost',   type = 'string', **_kw),
        dict(id = 'ogNutAlertStatusStatus', type = 'string', **_kw),
    )

    _relations = (
        ('SerialConsoleDev',
            ToOne(ToManyCont,
            'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
            'NutAlrt')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'NutAlert',
        'meta_type'      : 'NutAlert',
        'description'    : 'Opengear Nut Alert info',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addNutAlert',
        'immediate_view' : 'nutAlertPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'nutAlertPerformance',
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

InitializeClass(NutAlert)
