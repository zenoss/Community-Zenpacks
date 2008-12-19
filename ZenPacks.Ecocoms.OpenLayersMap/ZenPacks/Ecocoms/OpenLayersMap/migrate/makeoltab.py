#
# This class is only needed if you have a menu item instead of a tab (or both). 
#If you just use a tab then you can delete this before installing your zenpack
#
import Globals
import transaction
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPack
from AccessControl import Permissions as permissions


class makeoltab:
    version = Version(1, 0, 1)
    olMapTab = { 'id'            : 'olgeomaptab'
                , 'name'          : 'OpenLayers Map'
                , 'action'        : 'OLGeoMapTab'
                , 'permissions'   : (permissions.view,)
                }

    def _registerOLMapTab(self, dmd):
        # actions = list(dmd.Locations.factory_type_information[0]['actions'])
        # for i in range(len(actions)):
            # if(self.olMapTab['id'] in actions[i].values()):
                # return
        # actions.append(self.olMapTab)
        # dmd.Locations.factory_type_information[0]['actions'] = tuple(actions)
        # transaction.commit()
        # print "Reg: ",dmd.Locations.factory_type_information
        pass


    def migrate(self, pack):
        # dmd = pack.__primary_parent__.__primary_parent__
        # self._registerOLMapTab(dmd)
        pass

    def recover(self, pack):
        pass

 
makeoltab()
