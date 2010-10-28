################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenUtils.Utils import convToUnits

from Products.ZenRelations.RelSchema import *

from Products.ZenModel.HWComponent import HWComponent
from Products.ZenModel.ZenossSecurity import *

def manage_addHardDisk(context, id, title = None, REQUEST = None):
    """make a filesystem"""
    hd = HardDisk(id, title)
    context._setObject(id, hd)
    hd = context._getOb(id)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main')

addHardDisk = DTMLFile('dtml/addHardDisk',globals())

class StoragePool(HWComponent):

    portal_type = meta_type = 'StoragePool'

    manage_editHardDiskForm = DTMLFile('dtml/manageEditHardDisk',globals())

    description = ""
    hostresindex = 0
    size = 0
    status = 1

    _properties = HWComponent._properties + (
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'hostresindex', 'type':'int', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'status', 'type':'int', 'mode':'w'},
                )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW", "storagepools")),
        )


    factory_type_information = (
        {
            'id'             : 'StoragePool',
            'meta_type'      : 'StoragePool',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'DellEqualLogicMon',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewDellEqualLogicStoragePool',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellEqualLogicStoragePool'
                , 'permissions'   : (ZEN_VIEW,)
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

    def viewName(self): return self.description

    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size,divby=1000)

InitializeClass(StoragePool)
