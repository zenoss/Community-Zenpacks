###############################################################################
#
# ActiveUser object class
#
###############################################################################

__doc__ = """ ActiveUser

ActiveUser is a component of a SerialConsoleDevice

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

class ActiveUser(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'ActiveUser'

    ogSerialPortActiveUsersIndex = -1
    ogSerialPortActiveUsersPort = 0
    ogSerialPortActiveUsersName = ""
    snmpindex = -1

    _properties = (
        dict(id = 'ogSerialPortActiveUsersIndex', type = 'int',     **_kw),
        dict(id = 'ogSerialPortActiveUsersPort',  type = 'int',     **_kw),
        dict(id = 'ogSerialPortActiveUsersName',  type = 'string',	**_kw),
    )

    _relations = (
        ('SerialConsoleDev',
            ToOne(ToManyCont,
            'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
            'ActiveUsr')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'ActiveUser',
        'meta_type'      : 'ActiveUser',
        'description'    : 'Opengear Active User info',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addActiveUser',
        'immediate_view' : 'activeUserPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'activeUserPerformance',
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

InitializeClass(ActiveUser)
