from Globals import InitializeClass
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *

class WebSite(DeviceComponent, ManagedEntity):
    "Individual website on a webserver"
    
    portal_type = meta_type = "WebSite"
    
    url = ""
    
    _properties = (
        {'id':'url', 'type':'string', 'mode':''},
        )
    
    _relations = (
        ('webserver', ToOne(ToManyCont,
            'ZenPacks.example.Techniques.WebServerDevice', 'websites')),
        )
    
    factory_type_information = ({
        'id'             : 'WebSite',
        'meta_type'      : 'WebSite',
        'description'    : """Individual website on a webserver""",
        'icon'           : 'WebSite_icon.gif',
        'product'        : 'Techniques',
        'factory'        : 'manage_addWebSite',
        'immediate_view' : 'viewWebSite',
        'actions'        : (
            { 'id'            : 'status'
            , 'name'          : 'Status'
            , 'action'        : 'viewWebSite'
            , 'permissions'   : (ZEN_VIEW, )
            },
            { 'id'            : 'perfConf'
            , 'name'          : 'Template'
            , 'action'        : 'objTemplates'
            , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
            },                
            { 'id'            : 'viewHistory'
            , 'name'          : 'Modifications'
            , 'action'        : 'viewHistory'
            , 'permissions'   : (ZEN_VIEW, )
            },),
        },)
    
    def viewName(self):
        return self.id
    name = primarySortKey = viewName
    
    def device(self):
        return self.webserver()

InitializeClass(WebSite)
