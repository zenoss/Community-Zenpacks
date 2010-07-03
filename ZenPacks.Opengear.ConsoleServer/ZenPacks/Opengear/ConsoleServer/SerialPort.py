###############################################################################
#
# SerialPort object class
#
###############################################################################

__doc__ = """ SerialPort

SerialPort is a component of a SerialConsoleDevice

$id: $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class SerialPort(DeviceComponent, ManagedEntity):
    """ Serial console on an Opengear device

    """

    portal_type = meta_type = 'SerialPort'

    #serialPortIndex = -1
    serialPortNumber = 0
    serialPortLabel = ""
    serialPortMode = ""
    serialPortLoglevel = 0
    serialPortSpeed = 0
    serialPortCharsize = 0
    serialPortStop = 0
    serialPortParity = ""
    serialPortFlowcontrol = ""
    serialPortProtocol = ""
    serialPortTerminal = ""
    serialPortSsh = False
    serialPortTelnet = False
    serialPortRfc2217 = False
    serialPortRawtcp = False
    serialPortModeSummary = ""
    serialPortSettingSummary = ""

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
    #dcd = False
    #dtr = False
    #dsr = False
    #cts = False
    #rts = False

    snmpindex = -1

    _properties = (
        #dict(id = 'snmpindex',               type = 'int',     **_kw),
        dict(id = 'serialPortNumber',        type = 'int',     **_kw),
        dict(id = 'serialPortLabel',         type = 'string',  **_kw),
        dict(id = 'serialPortMode',          type = 'string',  **_kw),
        dict(id = 'serialPortLoglevel',      type = 'int',     **_kw),
        dict(id = 'serialPortSpeed',         type = 'int',     **_kw),
        dict(id = 'serialPortCharsize',      type = 'int',     **_kw),
        dict(id = 'serialPortStop',          type = 'int',     **_kw),
        dict(id = 'serialPortParity',        type = 'string',  **_kw),
        dict(id = 'serialPortFlowcontrol',   type = 'string',  **_kw),
        dict(id = 'serialPortProtocol',      type = 'string',  **_kw),
        dict(id = 'serialPortTerminal',      type = 'string',  **_kw),
        dict(id = 'serialPortSsh',           type = 'boolean', **_kw),
        dict(id = 'serialPortTelnet',        type = 'boolean', **_kw),
        dict(id = 'serialPortRfc2217',       type = 'boolean', **_kw),
        dict(id = 'serialPortRawtcp',        type = 'boolean', **_kw),
        dict(id = 'serialPortModeSummary',   type = 'string',  **_kw),
        dict(id = 'serialPortSettingSummary',type = 'string',  **_kw),
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
        #dict(id = 'dcd',                        type = 'boolean', **_kw),
        #dict(id = 'dtr',                        type = 'boolean', **_kw),
        #dict(id = 'dsr',                        type = 'boolean', **_kw),
        #dict(id = 'cts',                        type = 'boolean', **_kw),
        #dict(id = 'rts',                        type = 'boolean', **_kw),
    )

    _relations = (
        ('SerialConsoleDev', ToOne(ToManyCont,
            'ZenPacks.Opengear.ConsoleServer.SerialConsoleDevice',
            'SerialPrt')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = ({
        'id'             : 'SerialPort',
        'meta_type'      : 'SerialPort',
        'description'    : 'Opengear Serial Port',
        'icon'           : 'Device_icon.gif',
        'product'        : 'ConsoleServer',
        'factory'        : 'manage_addSerialPort',
        'immediate_view' : 'serialPortPerformance',
        'actions'        : ({
            'id'            : 'perf',
            'name'          : 'perf',
            'action'        : 'serialPortPerformance',
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
        d = self.getDmdRoot("Devices").findDevice(self.serialPortLabel)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def getPerformanceLink(self):
        from Products.ZenModel.ZenModelRM import ZenModelRM
        d = self.getDmdRoot("Devices").findDevice(self.serialPortLabel)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

InitializeClass(SerialPort)
