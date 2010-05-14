################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVADeviceHW

HPEVADeviceHW is an abstraction of a HP EVA Hardware

$Id: HPEVADeviceHW.py,v 1.0 2010/03/10 12:31:47 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenModel.Hardware import Hardware
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class HPEVADeviceHW(DeviceHW):

    # Define new relationships
    _relations = Hardware._relations + (
        ("cpus", ToManyCont(ToOne, "Products.ZenModel.CPU", "hw")),
        ("cards", ToManyCont(ToOne, "Products.ZenModel.ExpansionCard", "hw")),
        ("harddisks", ToManyCont(ToOne, "ZenPacks.community.HPEVAMon.HPEVADiskDrive", "hw")),
        ("fans", ToManyCont(ToOne, "Products.ZenModel.Fan", "hw")),
        ("powersupplies", ToManyCont(ToOne, "Products.ZenModel.PowerSupply",
            "hw")),
        ("temperaturesensors", ToManyCont(ToOne,
            "Products.ZenModel.TemperatureSensor", "hw")),
        ("enclosures", ToManyCont(ToOne,
	    "ZenPacks.community.HPEVAMon.HPEVAStorageDiskEnclosure", "hw")),
        ("fcports", ToManyCont(ToOne,
	    "ZenPacks.community.HPEVAMon.HPEVAHostFCPort", "hw")),
    )

    factory_type_information = (
        {
            'id'             : 'Device',
            'meta_type'      : 'Device',
            'description'    : """Base class for all devices""",
            'icon'           : 'Device_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addDevice',
            'immediate_view' : 'hpevaDeviceHardwareDetail',
            'actions'        : ()
         },
        )

    def __init__(self):
        id = "hw"
        Hardware.__init__(self, id)

InitializeClass(HPEVADeviceHW)
