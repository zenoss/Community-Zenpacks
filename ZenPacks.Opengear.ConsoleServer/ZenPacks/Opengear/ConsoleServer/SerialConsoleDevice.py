from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenRelations.RelSchema import *

import copy

class SerialConsoleDevice(Device):
    """ Opengear Serial Console Server
    """

    _relations = Device._relations + (
        ('SerialPrt', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.SerialPort", "SerialConsoleDev")),
        ('RpcCfg', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.Rpc", "SerialConsoleDev")),
        ('EmdCfg', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.Emd", "SerialConsoleDev")),
        ('UpsCfg', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.Ups", "SerialConsoleDev")),
        #('SerialPrtStat', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.SerialPortStatus", "SerialConsoleDev")),
        #('ActiveUsr', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.ActiveUser", "SerialConsoleDev")),
        #('RpcStat', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.RpcStatus", "SerialConsoleDev")),
        #('EmdStat', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.EmdStatus", "SerialConsoleDev")),
        #('SignalAlrt', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.SignalAlert", "SerialConsoleDev")),
        #('EnvironmentAlrt', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.EnvironmentAlert", "SerialConsoleDev")),
        #('NutAlrt', ToManyCont(ToOne, "ZenPacks.Opengear.ConsoleServer.NutAlert", "SerialConsoleDev")),
    )

    factory_type_information = ({
        'immediate_view' : 'deviceStatus',
        'actions'        : ({
            'id'            : 'status',
            'name'          : 'Status',
            'action'        : 'deviceStatus',
            'permissions'   : (ZEN_VIEW,)
        }, {
            'id'            : 'osdetail',
            'name'          : 'OS',
            'action'        : 'deviceOsDetail',
            'permissions'   : (ZEN_VIEW,)
        }, {
            'id'            : 'SerialPrt',
            'name'          : 'Serial Ports',
            'action'        : 'serialPortData',
            'permissions'   : (ZEN_VIEW,)
        }, {
            'id'            : 'RpcCfg',
            'name'          : 'RPCs',
            'action'        : 'rpcData',
            'permissions'   : (ZEN_VIEW,)
        }, {
            'id'            : 'UpsStat',
            'name'          : 'UPSs',
            'action'        : 'upsData',
            'permissions'   : (ZEN_VIEW,)
        }, {
            'id'            : 'EmdCfg',
            'name'          : 'EMDs',
            'action'        : 'emdData',
            'permissions'   : (ZEN_VIEW,)
        }, {
            'id'            : 'hwdetail',
            'name'          : 'Hardware',
            'action'        : 'deviceHardwareDetail',
            'permissions'   : (ZEN_VIEW,)
        }, {
            'id'            : 'events',
            'name'          : 'Events',
            'action'        : 'viewEvents',
            'permissions'   : (ZEN_VIEW,)
        }, {
            'id'            : 'perfServer',
            'name'          : 'Perf',
            'action'        : 'viewDevicePerformance',
            'permissions'   : (ZEN_VIEW,)
        }, {
            'id'            : 'edit',
            'name'          : 'Edit',
            'action'        : 'editDevice',
            'permissions'   : ("Change Device",)
        },)
    },)

InitializeClass(SerialConsoleDevice)
