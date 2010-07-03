###############################################################################
#
# Ups object class
#
###############################################################################

__doc__ = """ Ups

Ups is a component of a SerialConsoleDevice

$id: $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class Ups(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'Ups'

    upsName = ""
    upsDescription = ""
    upsType = ""
    upsAddress = ""
    upsConnected = ""
    upsLogStatus = ""
    ogUpsStatusFrequency = 0
    ogUpsStatusBatteryCharge = 0
    ogUpsStatusInputVoltage = 0
    ogUpsStatusLoad = 0
    ogUpsStatusOnline = 0
    ogUpsStatusTemperature = 0
    snmpindex = -1

    _properties = (
        dict(id = 'upsName',            type = 'string',	**_kw),
        dict(id = 'upsDescription',     type = 'string',	**_kw),
        dict(id = 'upsType',            type = 'string',	**_kw),
        dict(id = 'upsAddress',         type = 'string',	**_kw),
        dict(id = 'upsConnected',       type = 'string',	**_kw),
        dict(id = 'upsLogStatus',       type = 'string',	**_kw),
        dict(id = 'snmpindex',          type = 'int',	    **_kw),
    )

    _relations = (
        ('SerialConsoleDev',
            ToOne(ToManyCont,
            'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
            'UpsCfg')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'Ups',
        'meta_type'      : 'Ups',
        'description'    : 'Opengear UPS info',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addUps',
        'immediate_view' : 'upsPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'upsPerformance',
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
        d = self.getDmdRoot("Devices").findDevice(self.upsName)
        if d:
            return ZenModelRM.urlLink(d, 'link')

    def getPerformanceLink(self):
        from Products.ZenModel.ZenModelRM import ZenModelRM
        d = self.getDmdRoot("Devices").findDevice(self.upsName)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

InitializeClass(Ups)
