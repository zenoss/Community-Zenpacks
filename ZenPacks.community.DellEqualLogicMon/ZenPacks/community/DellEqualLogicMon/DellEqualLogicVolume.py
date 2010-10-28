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

from Products.ZenUtils.Utils import prepId

import logging
log = logging.getLogger("zen.DellEqualLogicVolume")

def manage_addVolume(context, id, userCreated, REQUEST=None):
    svid = prepId(id)
    sv = DellEqualLogicVolume(svid)
    context._setObject(svid, sv)
    sv = context._getOb(svid)
    if userCreated: sv.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sv

class DellEqualLogicVolume(OSComponent, DellEqualLogicComponent):

    portal_type = meta_type = 'DellEqualLogicVolume'

    caption = ""
    volumeProvisionedSize = 0 
    volumeReservedSize = 0
    thinProvisioned = 2
    state = "OK"

    _properties = OSComponent._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
		 {'id':'volumeProvisionedSize', 'type':'int', 'mode':'w'},
		 {'id':'volumeReservedSize', 'type':'int', 'mode':'w'},
		 {'id':'thinProvisioned', 'type':'int', 'mode':'w'},
                )

    _relations = OSComponent._relations + (
        ("os", ToOne(
            ToManyCont,
            "ZenPacks.community.DellEqualLogicMon.DellEqualLogicDevice.DellEqualLogicDeviceOS",
            "volumes")),
        )

    factory_type_information = (
        {
            'id'             : 'Volume',
            'meta_type'      : 'Volume',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StoragePool_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addVolume',
            'immediate_view' : 'viewDellEqualLogicVolume',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellEqualLogicVolume'
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

    def reservedSize(self):
	return self.volumeReservedSize or 0

    def reservedSizeString(self):
	return convToUnits(self.reservedSize(), divby=1024)

    def provisionedSize(self):
	return self.volumeProvisionedSize or 0

    def provisionedSizeString(self):
	return convToUnits(self.provisionedSize(), divby=1024)

    def isThinProvisioned(self):
	if (self.thinProvisioned == 1):
	    return "true"
	else:
	    return "false"

#    def getRRDNames(self):
#        return ['Volume_Occupancy']

InitializeClass(DellEqualLogicVolume)
