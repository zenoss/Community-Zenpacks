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
        portletsrc = zenPath('ZenPacks','ZenPacks.Ecocoms.OpenLayersMap-1.0-py2.4.egg','ZenPacks','Ecocoms','OpenLayersMap','OLMapsPortlet.js')
        zpm.register_portlet( sourcepath=portletsrc, id='OpenLayersMapPortlet',
                        title='OpenLayers Map', permission=ZEN_COMMON)
        # Register new tab in locations
        dmd = self.getDmdRoot('Locations')
        actions = list(dmd.factory_type_information[0]['actions'])
        for i in range(len(actions)):
            if(self.olMapTab['id'] in actions[i].values()):
                return
        actions.append(self.olMapTab)
        dmd.Locations.factory_type_information[0]['actions'] = tuple(actions)
        transaction.commit()
        print "Reg: ",dmd.factory_type_information

    # def _registerOLMapTab(self, app):
        # actions = list(self.dmd.Locations.factory_type_information[0]['actions'])
        # for i in range(len(actions)):
            # if(self.olMapTab['id'] in actions[i].values()):
                # return
        # actions.append(self.olMapTab)
        # self.dmd.Locations.factory_type_information[0]['actions'] = tuple(actions)
        # transaction.commit()
        # print "Reg: ",self.dmd.Locations.factory_type_information


    # def _unregisterOLMapTab(self, app):
        # actions = list(self.dmd.Locations.factory_type_information[0]['actions'])
        # for i in range(len(actions)):
            # if(self.olMapTab['id'] in actions[i].values()):
                # actions.remove(actions[i])
        # self.dmd.Locations.factory_type_information[0]['actions'] = tuple(actions)
        # transaction.commit()
        # print "unReg: ",self.dmd.Locations.factory_type_information
           
    def install(self, app):
        ZenPackBase.install(self, app)
        self._registerOLMapPortlet(app)
#        self._registerOLMapTab(app)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self._registerOLMapPortlet(app)
#        self._unregisterOLMapTab(app)        
#        self._registerOLMapTab(app)
        
    def remove(self, app):
        ZenPackBase.remove(self, app)
        zpm = app.zport.ZenPortletManager
        zpm.unregister_portlet('OpenLayersMapPortlet')
#        self._unregisterOLMapTab(app)
