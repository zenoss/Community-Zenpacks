###############################################################################
#
# Emd object class
#
###############################################################################

__doc__ = """ Emd

Emd is a component of a SerialConsoleDevice

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

class Emd(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'Emd'

    emdName = ""
    emdDescription = ""
    emdConnected = ""
    emdLogStatus = False
    emdEnabled = False
    snmpindex = -1

    _properties = (
        dict(id = 'emdName',        type = 'string',	 **_kw),
        dict(id = 'emdDescription', type = 'string',     **_kw),
        dict(id = 'emdConnected',   type = 'string',     **_kw),
        dict(id = 'emdLogStatus',   type = 'boolean',    **_kw),
        dict(id = 'emdEnabled',     type = 'boolean',    **_kw),
    )

    _relations = (
        ('SerialConsoleDev',
            ToOne(ToManyCont,
            'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
            'EmdCfg')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'Emd',
        'meta_type'      : 'Emd',
        'description'    : 'Opengear EMD info',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addEmd',
        'immediate_view' : 'emdPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'emdPerformance',
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
        d = self.getDmdRoot("Devices").findDevice(self.emdName)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def getPerformanceLink(self):
        from Products.ZenModel.ZenModelRM import ZenModelRM
        d = self.getDmdRoot("Devices").findDevice(self.emdName)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

InitializeClass(Emd)
