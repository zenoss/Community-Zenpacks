###############################################################################
#
# EmdStatus object class
#
###############################################################################

__doc__ = """ EmdStatus

EmdStatus is a component of a SerialConsoleDevice

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

class EmdStatus(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'EmdStatus'

    ogEmdStatusIndex = -1
    ogEmdStatusName = ""
    ogEmdStatusTemp = 0
    ogEmdStatusHumidity = 0
    ogEmdStatusAlertCount = 0
    snmpindex = -1

    _properties = (
        dict(id = 'ogEmdStatusIndex',      type = 'int',     **_kw),
        dict(id = 'ogEmdStatusName',       type = 'string',	**_kw),
        dict(id = 'ogEmdStatusTemp',       type = 'int',     **_kw),
        dict(id = 'ogEmdStatusHumidity',   type = 'int',     **_kw),
        dict(id = 'ogEmdStatusAlertCount', type = 'int',     **_kw),
    )

    _relations = (
        ('SerialConsoleDev',
            ToOne(ToManyCont,
            'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
            'EmdStat')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'EmdStatus',
        'meta_type'      : 'EmdStatus',
        'description'    : 'Opengear EMD info',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addEmdStatus',
        'immediate_view' : 'emdStatusPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'emdStatusPerformance',
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

InitializeClass(EmdStatus)
