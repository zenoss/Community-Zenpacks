from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class Terminal(DeviceComponent, ManagedEntity):
    "tty device on the console server"
    
    portal_type = meta_type = 'Terminal'

    deviceName = "ttySxx"
    serverAlias = ""
    txBytes = 0
    rxBytes = 0
    connected = False
    up = False
    snmpindex = -1

    _properties = (
        dict(id='deviceName',	type='string',	**_kw),
        dict(id='serverAlias',  type='string',	**_kw),
        dict(id='txBytes',  	type='int',	**_kw),
        dict(id='rxBytes',  	type='int',	**_kw),
        dict(id='snmpindex',  	type='int',	**_kw),
        dict(id='connected', 	type='boolean',	**_kw),
        dict(id='up', 		type='boolean',	**_kw),
        )

    _relations = (
        ('host', ToOne(ToManyCont, 
        'ZenPacks.chudler.AlterPathCS.Terminal', 
            'terminals')),
        )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
        {
            'id'             : 'Terminal',
            'meta_type'      : 'Terminal',
            'description'    : 'Terminal Description',
            'icon'           : 'Device_icon.gif',
            'product'        : 'AlterPathCS',
            'factory'        : 'manage_addTerminal',
            'immediate_view' : 'terminalPerformance',
            'actions'        :
            (
                { 'id'            : 'perf'
                , 'name'          : 'perf'
                , 'action'        : 'terminalPerformance'
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
        return self.host()

    def managedDeviceLink(self):
        from Products.ZenModel.ZenModelRM import ZenModelRM
        d = self.getDmdRoot("Devices").findDevice(self.serverAlias)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
    

InitializeClass(Terminal)
