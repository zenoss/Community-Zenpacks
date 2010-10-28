################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Globals import DTMLFile, InitializeClass
from Products.ZenModel.OSComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from DellEqualLogicComponent import *

from Products.ZenUtils.Utils import convToUnits

class DellEqualLogicStoragePool(OSComponent, DellEqualLogicComponent):

    #portal_type = meta_type = 'StoragePool'
    portal_type = meta_type = 'DellEqualLogicStoragePool'

    caption = ""
    poolSpace = 0
    poolUsedSpace = 0
    state = "OK"

    _properties = OSComponent._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
		 		 {'id':'poolSpace', 'type':'int', 'mode':'w'},
				 {'id':'poolUsedSpace', 'type':'int', 'mode':'w'},
                )

    _relations = OSComponent._relations + (
        ("os", ToOne(
            ToManyCont,
            "ZenPacks.community.DellEqualLogicMon.DellEqualLogicDevice.DellEqualLogicDeviceOS",
            "storagepools")),
        )

    factory_type_information = (
        {
            'id'             : 'StoragePool',
            'meta_type'      : 'StoragePool',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StoragePool_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addStoragePool',
            'immediate_view' : 'viewDellEqualLogicStoragePool',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellEqualLogicStoragePool'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

    def totalBytes(self):
        return self.poolSpace or 0

    def totalBytesString(self):
        return convToUnits(self.totalBytes(), divby=1024)

    def usedBytes(self):
        return self.poolUsedSpace or 0

    def usedBytesString(self):
        return convToUnits(self.usedBytes(), divby=1024)

    def getRRDNames(self):
        """
        Return the datapoint name of this StoragePool
        """
        return ['StoragePool_Occupancy']

	def getRRDTemplates(self):
		templates = []
		for tname in [self.__class__.__name__]:
			templ = self.getRRDTemplateByName(tname)
			if templ: templates.append(templ)
		return templates

InitializeClass(DellEqualLogicStoragePool)
