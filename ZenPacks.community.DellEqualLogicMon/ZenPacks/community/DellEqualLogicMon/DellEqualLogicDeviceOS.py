################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################


from Globals import InitializeClass
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.Software import Software
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class DellEqualLogicDeviceOS(OperatingSystem):

    # Define new relationships
    _relations = Software._relations + (
        ("interfaces", ToManyCont(ToOne,
            "Products.ZenModel.IpInterface", "os")),
        ("routes", ToManyCont(ToOne, "Products.ZenModel.IpRouteEntry", "os")),
        ("ipservices", ToManyCont(ToOne, "Products.ZenModel.IpService", "os")),
        ("winservices", ToManyCont(ToOne,
            "Products.ZenModel.WinService", "os")),
        ("processes", ToManyCont(ToOne, "Products.ZenModel.OSProcess", "os")),
        ("filesystems", ToManyCont(ToOne,
            "Products.ZenModel.FileSystem", "os")),
        ("software", ToManyCont(ToOne, "Products.ZenModel.Software", "os")),
        ("storagepools", ToManyCont(ToOne,
            "ZenPacks.community.DellEqualLogicMon.DellEqualLogicStoragePool", "os")),
	("volumes", ToManyCont(ToOne,
	    "ZenPacks.community.DellEqualLogicMon.DellEqualLogicVolume", "os")),
    )


    factory_type_information = (
        {
            'id'             : 'Device',
            'meta_type'      : 'Device',
            'description'    : """Base class for all devices""",
            'icon'           : 'Device_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addDevice',
            'immediate_view' : 'dellEqualLogicDeviceOsDetail',
            'actions'        : ()
         },
        )


    def __init__(self):
        id = "os"
        Software.__init__(self, id)
        self._delObject("os")   # OperatingSystem is a software 
                                # but doens't have os relationship


InitializeClass(DellEqualLogicDeviceOS)
