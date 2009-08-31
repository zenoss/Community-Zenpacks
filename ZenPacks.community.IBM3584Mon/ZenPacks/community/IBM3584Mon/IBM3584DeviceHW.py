from Globals import InitializeClass
from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class IBM3584DeviceHW(DeviceHW):

    # Define new relationships
    _relations = DeviceHW._relations + (
        ("changerdevices", ToManyCont(ToOne, "ZenPacks.community.IBM3584Mon.IBM3584ChangerDevice", "hw")),
        ("frames", ToManyCont(ToOne, "ZenPacks.community.IBM3584Mon.IBM3584Frame", "hw")),
        ("accessdevices", ToManyCont(ToOne, "ZenPacks.community.IBM3584Mon.IBM3584AccessDevice", "hw")),
    )

InitializeClass(IBM3584DeviceHW)

