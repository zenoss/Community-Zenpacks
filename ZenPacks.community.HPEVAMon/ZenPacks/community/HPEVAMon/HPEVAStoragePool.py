################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStoragePool

HPEVAStoragePool is an abstraction of a HPEVA_StoragePool

$Id: HPEVAStoragePool.py,v 1.3 2010/06/30 17:10:54 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from Products.ZenModel.OSComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

from Products.ZenUtils.Utils import convToUnits

class HPEVAStoragePool(OSComponent, HPEVAComponent):
    """HPStoragePool object"""

    portal_type = meta_type = 'HPEVAStoragePool'

    caption = ""
    diskGroupType = ""
    diskType = ""
    protLevel = ""
    totalManagedSpace = 0
    totalDisks = 0
    threshold = 0
    state = "OK"

    _properties = OSComponent._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'diskGroupType', 'type':'string', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'protLevel', 'type':'string', 'mode':'w'},
                 {'id':'totalManagedSpace', 'type':'int', 'mode':'w'},
                 {'id':'totalDisks', 'type':'int', 'mode':'w'},
                 {'id':'threshold', 'type':'int', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
                )


    _relations = OSComponent._relations + (
        ("os", ToOne(
            ToManyCont,
            "ZenPacks.community.HPEVAMon.HPEVADevice.HPEVADeviceOS",
            "storagepools")),
        ("harddisks", ToMany(
            ToOne,
            "ZenPacks.community.HPEVAMon.HPEVADiskDrive",
            "storagepool")),
        ("virtualdisks", ToMany(
            ToOne,
            "ZenPacks.community.HPEVAMon.HPEVAStorageVolume",
            "storagepool")),
        )

    factory_type_information = ( 
        {
            'id'             : 'StoragePool',
            'meta_type'      : 'StoragePool',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StoragePool_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addStoragePool',
            'immediate_view' : 'viewHPEVAStoragePool',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVAStoragePool'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'disks'
                , 'name'          : 'Disks'
                , 'action'        : 'viewHPEVAStoragePoolDisks'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'volumes'
                , 'name'          : 'Volumes'
                , 'action'        : 'viewHPEVAStoragePoolVolumes'
                , 'permissions'   : (ZEN_VIEW, )
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
        return self.totalManagedSpace or 0

    def usedBytes(self):
        return self.cacheRRDValue('Occupancy', 0)

    def totalBytesString(self):
        return convToUnits(self.totalBytes(), divby=1024)

    def usedBytesString(self):
        return convToUnits(self.usedBytes(), divby=1024)

    def availBytesString(self):
        return convToUnits((self.totalBytes() - self.usedBytes()), divby=1024)

    def capacity(self):
        """
        Return the percentage capacity of a filesystems using its rrd file
        """
        __pychecker__='no-returnvalues'
        if self.totalBytes() is not 0:
            return int(100.0 * self.usedBytes() / self.totalBytes())
        return 'unknown'

    def disks(self):
        return self.totalDisks or 0

    def getRRDNames(self):
        """
        Return the datapoint name of this StoragePool
        """
        return ['StoragePool_Occupancy']

InitializeClass(HPEVAStoragePool)
