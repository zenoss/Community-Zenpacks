from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from Products.ZenModel.Device import Device

from ZenPacks.example.Techniques.WebSite import WebSite

class WebServerDevice(Device):
    "A device that contains zero or more websites"
    
    _relations = Device._relations + (
        ('websites', ToManyCont(ToOne,
            'ZenPacks.example.Techniques.WebSite', 'webserver')),
        )
    
    security = ClassSecurityInfo()
    
    def __init__(self, *args, **kwargs):
        Device.__init__(self, *args, **kw)
        self.buildRelations()
    
    security.declareProtected(ZEN_MANAGE_DMD, 'manage_addWebSite')
    def manage_addWebSite(self, id, url, REQUEST=None):
        """Add a web site to this web server"""
        if not id: return self.callZenScreen(REQUEST)
        website = WebSite(id)
        self.websites._setObject(id, website)
        website = self.websites._getOb(id)
        website.url = url
        website.index_object()
        if REQUEST:
            if website:
                REQUEST['message'] = "WebSite %s added" % website.id
                url = "%s/websites/%s" % (self.getPrimaryUrlPath(), website.id)
                return REQUEST['RESPONSE'].redirect(url)
            else:
                return self.callZenScreen(REQUEST)
        return website
        

InitializeClass(WebServerDevice)