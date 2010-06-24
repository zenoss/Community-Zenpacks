from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class ZeusVirtualServer(DeviceComponent, ManagedEntity):
    "Zeus Virtual Server Information"
    
    portal_type = meta_type = 'ZeusVirtualServer'

    vsName = ""
    vsPort = 0
    vsProtocol = ""
    snmpindex = -1

    _properties = (
        dict(id='vsName', type='string',  **_kw),
        dict(id='vsPort', type='int',  **_kw),
        dict(id='vsProtocol', type='string',  **_kw)
    )

    _relations = (
        ('zeus', ToOne(ToManyCont, 'ZenPacks.community.ZeusLoadBalancer.ZeusLoadBalancer', 'virtualServers')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
        {
            'id'             : 'ZeusVirtualServer',
            'meta_type'      : 'Zeus Virtual Server',
            'description'    : 'Zeus Virtual Server Description',
            'icon'           : 'Device_icon.gif',
            'product'        : 'ZeusVirtualServers',
            'factory'        : 'manage_addZeusVS',
            'immediate_view' : 'zeusVSPerformance',
            'actions'        :
            (
                { 'id'            : 'perf'
                , 'name'          : 'perf'
                , 'action'        : 'zeusVSPerformance'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'templates'
                , 'name'          : 'Templates'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                },
            )
        },
    )

    def device(self):
        return self.zeus()

    def managedDeviceLink(self):
        from Products.ZenModel.ZenModelRM import ZenModelRM
        d = self.getDmdRoot("Devices").findDevice(self.vsName)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
    

InitializeClass(ZeusVirtualServer)
