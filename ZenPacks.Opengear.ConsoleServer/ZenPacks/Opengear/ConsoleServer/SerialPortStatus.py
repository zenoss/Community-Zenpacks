###############################################################################
#
# SerialPortStatus object class
#
###############################################################################

__doc__ = """ SerialPortStatus

SerialPortStatus is a component of a SerialConsoleDevice

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

class SerialPortStatus(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'SerialPortStatus'

    ogSerialPortStatusIndex = -1
    ogSerialPortStatusPort = 0
    ogSerialPortStatusRxBytes = 0
    ogSerialPortStatusTxBytes = 0
    ogSerialPortStatusSpeed = 0
    ogSerialPortStatusDCD = 0
    ogSerialPortStatusDTR = 0
    ogSerialPortStatusDSR = 0
    ogSerialPortStatusCTS = 0
    ogSerialPortStatusRTS = 0
    dcd = False
    dtr = False
    dsr = False
    cts = False
    rts = False
    snmpindex = -1

    _properties = (
        #dict(id = 'snmpindex',   type = 'int',     **_kw),
        dict(id = 'ogSerialPortStatusIndex',    type = 'int',     **_kw),
        dict(id = 'ogSerialPortStatusPort',     type = 'int',     **_kw),
        dict(id = 'ogSerialPortStatusRxBytes',  type = 'int',	  **_kw),
        dict(id = 'ogSerialPortStatusTxBytes',  type = 'int',	  **_kw),
        dict(id = 'ogSerialPortStatusSpeed',    type = 'int',     **_kw),
        dict(id = 'ogSerialPortStatusDCD',      type = 'int',     **_kw),
        dict(id = 'ogSerialPortStatusDTR',      type = 'int',     **_kw),
        dict(id = 'ogSerialPortStatusDSR',      type = 'int',     **_kw),
        dict(id = 'ogSerialPortStatusCTS',      type = 'int',     **_kw),
        dict(id = 'ogSerialPortStatusRTS',      type = 'int',     **_kw),
        dict(id = 'dcd',                        type = 'boolean', **_kw),
        dict(id = 'dtr',                        type = 'boolean', **_kw),
        dict(id = 'dsr',                        type = 'boolean', **_kw),
        dict(id = 'cts',                        type = 'boolean', **_kw),
        dict(id = 'rts',                        type = 'boolean', **_kw),
    )

    _relations = (
        ('SerialConsoleDev',
         ToOne(ToManyCont,
               'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
               'SerialPortStat')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'SerialPortStatus',
        'meta_type'      : 'SerialPortStatus',
        'description'    : 'Opengear Serial Port info',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addSerialPortStatus',
        'immediate_view' : 'serialPortStatusPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'serialPortStatusPerformance',
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
        d = self.getDmdRoot("Devices").findDevice(self.serverAlias)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def getPerformanceLink(self):
        #from Products.ZenModel.ZenModelRM import ZenModelRM
        #d = self.getDmdRoot("Devices").findDevice(self.serialPortLabel)
        #if d:
        #    return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

InitializeClass(SerialPortStatus)
