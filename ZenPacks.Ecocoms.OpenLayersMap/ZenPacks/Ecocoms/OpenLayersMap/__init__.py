import Globals
import transaction
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())


from AccessControl import Permissions as permissions
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import zenPath
from Products.ZenModel.ZenossSecurity import *
from Products.ZenUtils.ZenScriptBase import ZenScriptBase 

class ZenPack(ZenPackBase):
    olMapTab = { 'id'            : 'olgeomaptab'
                , 'name'          : 'OpenLayers Map'
                , 'action'        : 'OLGeoMapTab'
                , 'permissions'   : (permissions.view,)
                }

    def _registerOLMapPortlet(self, app):
        zpm = app.zport.ZenPortletManager
        portletsrc = zenPath('ZenPacks','ZenPacks.Ecocoms.OpenLayersMap-1.1-py2.4.egg','ZenPacks','Ecocoms','OpenLayersMap','OLMapsPortlet.js')
        zpm.register_portlet( sourcepath=portletsrc, id='OpenLayersMapPortlet',
                        title='OpenLayers Map', permission=ZEN_COMMON)

    def _registerOLMapTab(self, app):
        # Register new tab in locations
        dmdloc = self.getDmdRoot('Locations')
        finfo = dmdloc.factory_type_information 
        actions = list(finfo[0]['actions'])
        for i in range(len(actions)):
            if(self.olMapTab['id'] in actions[i].values()):
                return
        actions.append(self.olMapTab)
        finfo[0]['actions'] = tuple(actions)
        dmdloc.factory_type_information = finfo
        transaction.commit()
        print "Reg: ",dmdloc.factory_type_information


    def _unregisterOLMapTab(self, app):
        dmdloc = self.getDmdRoot('Locations')
        finfo = dmdloc.factory_type_information 
        actions = list(finfo[0]['actions'])
        for i in range(len(actions)):
            if(self.olMapTab['id'] in actions[i].values()):
                actions.remove(actions[i])
        finfo[0]['actions'] = tuple(actions)
        dmdloc.factory_type_information = finfo
        transaction.commit()
        print "unReg: ",self.dmd.Locations.factory_type_information
           
    def install(self, app):
        ZenPackBase.install(self, app)
        self._registerOLMapPortlet(app)
        #self._registerOLMapTab(app)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self._registerOLMapPortlet(app)
        #self._registerOLMapTab(app)
        
    def remove(self, app, leaveObjects):
        ZenPackBase.remove(self, app, leaveObjects)
        zpm = app.zport.ZenPortletManager
        zpm.unregister_portlet('OpenLayersMapPortlet')
        #self._unregisterOLMapTab(app)

