###############################################################################
#
# Rpc object class
#
###############################################################################

__doc__ = """ Rpc

Rpc is a component of a SerialConsoleDevice

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

class Rpc(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'Rpc'

    rpcName = ""
    rpcDescription = ""
    rpcType = ""
    rpcConnected = ""
    rpcLogStatus = ""
    snmpindex = -1

    _properties = (
        dict(id = 'rpcName',            type = 'string',	**_kw),
        dict(id = 'rpcDescription',     type = 'string',	**_kw),
        dict(id = 'rpcType',            type = 'string',	**_kw),
        dict(id = 'rpcConnected',       type = 'string',	**_kw),
        dict(id = 'rpcLogStatus',       type = 'string',	**_kw),
    )

    _relations = (
        ('SerialConsoleDev',
            ToOne(ToManyCont,
            'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
            'RpcCfg')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'Rpc',
        'meta_type'      : 'Rpc',
        'description'    : 'Opengear RPC info',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addRpc',
        'immediate_view' : 'rpcPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'rpcPerformance',
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
        from Products.ZenModel.ZenModelRM import ZenModelRM
        d = self.getDmdRoot("Devices").findDevice(self.rpcName)
        if d:
            return ZenModelRM.urlLink(d, 'link')

    def getPerformanceLink(self):
        from Products.ZenModel.ZenModelRM import ZenModelRM
        d = self.getDmdRoot("Devices").findDevice(self.rpcName)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

InitializeClass(Rpc)
