from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class ZeusPool(DeviceComponent, ManagedEntity):
    "Zeus Pool Information"
    
    portal_type = meta_type = 'ZeusPool'

    poolName = ""
    poolAlgorithm = ""
    poolNodes = -1
    poolDraining = -1
    poolFailPool = "None"
    poolPersistence = ""
    snmpindex = -1

    _properties = (
        dict(id='poolName', type='string',  **_kw),
        dict(id='poolAlgorithm', type='string',  **_kw),
        dict(id='poolNodes', type='int',  **_kw),
        dict(id='poolDraining', type='int',  **_kw),
        dict(id='poolFailPool', type='string',  **_kw),
        dict(id='poolPersistence',type='string',  **_kw)
    )

    _relations = (
        ('zeus', ToOne(ToManyCont, 'ZenPacks.community.ZeusLoadBalancer.ZeusLoadBalancer', 'pools')),
    )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
        {
            'id'             : 'ZeusPool',
            'meta_type'      : 'Zeus Pool',
            'description'    : 'Zeus Pool Description',
            'icon'           : 'Device_icon.gif',
            'product'        : 'ZeusPools',
            'factory'        : 'manage_addZeusPool',
            'immediate_view' : 'zeusPoolPerformance',
            'actions'        :
            (
                { 'id'            : 'perf'
                , 'name'          : 'perf'
                , 'action'        : 'zeusPoolPerformance'
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
        d = self.getDmdRoot("Devices").findDevice(self.poolName)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
    

InitializeClass(ZeusPool)
