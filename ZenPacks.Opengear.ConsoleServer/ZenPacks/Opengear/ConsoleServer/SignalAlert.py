###############################################################################
#
# SignalAlert object class
#
###############################################################################

__doc__ = """ SignalAlert

SignalAlert is a component of a SerialConsoleDevice

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

class SignalAlert(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'SignalAlert'

    ogSignalAlertStatusIndex = -1
    ogSignalAlertStatusPort = -1
    ogSignalAlertStatusLabel = ""
    ogSignalAlertStatusSignalName = ""
    ogSignalAlertStatusState = 0
    snmpindex = -1

    _properties = (
        dict(id = 'ogSignalAlertStatusIndex',     type = 'int',    **_kw),
        dict(id = 'ogSignalAlertStatusPort',      type = 'int',	   **_kw),
        dict(id = 'ogSignalAlertStatusLabel',     type = 'string', **_kw),
        dict(id = 'ogSignalAlertStatusSignalName',type = 'string', **_kw),
        dict(id = 'ogSignalAlertStatusState',     type = 'int',    **_kw),
    )

    _relations = (
        ('SerialConsoleDev',
            ToOne(ToManyCont,
            'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
            'SignalAlrt')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'SignalAlert',
        'meta_type'      : 'SignalAlert',
        'description'    : 'Opengear Serial Port Signal info',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addSignalAlert',
        'immediate_view' : 'signalAlertPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'signalAlertPerformance',
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

InitializeClass(SignalAlert)
